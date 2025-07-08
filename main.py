import sys
import pandas as pd
import traceback
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from recipe_ui import Ui_MainWindow
from modules.import_export import import_recipe, export_recipe
from modules.autosave import autosave_recipe
from modules.plc_interface import PLCInterface

import time


class RecipeSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 綁定事件
        self.ui.BoardNo.currentIndexChanged.connect(self.update_recipe_types)
        self.ui.RecipeType.currentIndexChanged.connect(self.update_subtypes)
        self.ui.Import.clicked.connect(self.handle_import)
        self.ui.Export.clicked.connect(self.handle_export)
        self.ui.Backup.clicked.connect(self.handle_backup)
        self.ui.Download.clicked.connect(self.handle_write)

        self.recipe_type_map = {
            "Common":  ["common_parameters", "alarm_settings", "calibration", "auto_sequence"],
            "Board-1": ["board_parameters", "alarm_settings", "calibration", "pid_parameters", "auto_sequence"],
            "Board-2": ["board_parameters", "alarm_settings", "calibration", "pid_parameters", "auto_sequence"],
            "Board-3": ["board_parameters", "alarm_settings", "calibration", "pid_parameters", "auto_sequence"],
            "Board-4": ["board_parameters", "alarm_settings", "calibration", "pid_parameters", "auto_sequence"]
        }

        self.subtype_map = {
            "calibration": ["flow_rate", "temperature", "pressure"],
            "auto_sequence": ["solvent", "polymerization", "replacement", "stop"],
            "alarm_settings": ["flow_rate", "temperature", "pressure"],
        }

        self.update_recipe_types()

    def log(self, message: str):
        self.ui.Log.append(message)

    def update_recipe_types(self):
        board = self.ui.BoardNo.currentText()
        types = self.recipe_type_map.get(board, [])
        self.ui.RecipeType.clear()
        self.ui.RecipeType.addItems(types)
        self.update_subtypes()

    def update_subtypes(self):
        rtype = self.ui.RecipeType.currentText()
        subtypes = self.subtype_map.get(rtype, [])
        self.ui.SubType.clear()
        self.ui.SubType.addItems(subtypes)

    def handle_import(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            try:
                msg = import_recipe(file_path, self.ui.RecipeType.currentText(), self.ui.RecipeName.text())
                self.log(msg)
            except Exception as e:
                self.log(f"[錯誤] {str(e)}")

    def handle_export(self):
        try:
            msg = export_recipe(self.ui.RecipeType.currentText(), self.ui.RecipeName.text())
            self.log(msg)
        except Exception as e:
            self.log(f"[錯誤] {str(e)}")

    def handle_backup(self):
        try:
            msg = autosave_recipe(self.ui.RecipeType.currentText(), self.ui.RecipeName.text())
            self.log(msg)
        except Exception as e:
            self.log(f"[錯誤] {str(e)}")

    def extract_scalar(self, val):
        self.log(f"🔍 原始型別: {type(val)}, 值: {val}")
        while isinstance(val, list):
            if len(val) == 0:
                raise ValueError("空 list 無法轉換")
            val = val[0]
        if hasattr(val, 'item'):
            val = val.item()
        return val

    def handle_write(self):
        try:
            start_time = time.time()
            self.log("開始寫入 PLC")
            plc = PLCInterface()
            from modules.import_export import RECIPE_DIR
            category = self.ui.RecipeType.currentText()
            name = self.ui.RecipeName.text()
            path = f"{RECIPE_DIR}/{category}/{name}.xlsx"

            df = pd.read_excel(path)

            address_list = df["Address"].tolist()
            value_list = [int(self.extract_scalar(v)) for v in df["Value"]]

            plc.write_device(address_list, value_list)
            elapsed_time = time.time() - start_time
            self.log(f"🕒 寫入 {len(address_list)} 筆資料總耗時：{elapsed_time:.3f} 秒")

            for addr, val in zip(address_list, value_list):
                self.log(f"✔️ 寫入 {addr} = {val}")

            self.log(f"✅ 完成寫入 PLC：{name}")
        except Exception as e:
            self.log(f"[錯誤] {str(e)}")
        finally:
            try:
                plc.close()
            except:
                pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RecipeSystem()
    window.show()
    sys.exit(app.exec_())
