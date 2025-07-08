import os
import pandas as pd
from datetime import datetime
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPE_DIR = os.path.join(BASE_DIR, 'recipes')
BACKUP_DIR = os.path.join(BASE_DIR, 'backup')

REQUIRED_COLUMNS = ["Tagname", "Address", "Value"]

def validate_recipe_format(df: pd.DataFrame, required_columns: list[str]) -> bool:
    """驗證匯入的 DataFrame 是否包含必要欄位"""
    return all(col in df.columns for col in required_columns)

def import_recipe(file_path: str, category: str, name: str, required_columns: list[str] = REQUIRED_COLUMNS) -> str:
    """
    將 Excel 檔匯入並儲存至指定分類資料夾中。
    會覆蓋舊檔並備份原始檔。
    """
    df = pd.read_excel(file_path, sheet_name=None)  # 讀取所有工作表

    if not df:
        raise ValueError("Excel 檔案中沒有任何工作表。")

    for sheet_name, sheet_df in df.items():
        if not validate_recipe_format(sheet_df, required_columns):
            raise ValueError(f"工作表 {sheet_name} 缺少必要欄位，匯入失敗。")

        recipe_path = os.path.join(RECIPE_DIR, category, f"{sheet_name}.xlsx")
        backup_path = os.path.join(BACKUP_DIR, category)
        os.makedirs(backup_path, exist_ok=True)

        if os.path.exists(recipe_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            backup_file = os.path.join(backup_path, f"{sheet_name}_{timestamp}.xlsx")
            os.rename(recipe_path, backup_file)

        sheet_df.to_excel(recipe_path, index=False)

    return f"成功匯入 {len(df)} 個工作表至 {category} 類別資料夾。"

def export_recipe(category: str, name: str, export_to: Optional[str] = None) -> str:
    """
    將指定 recipe 複製到 export_to 指定資料夾（或預設當前目錄），並加上時間戳記。
    """
    recipe_path = os.path.join(RECIPE_DIR, category, f"{name}.xlsx")
    if not os.path.exists(recipe_path):
        raise FileNotFoundError("找不到指定的 recipe 檔案。")

    df = pd.read_excel(recipe_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    export_filename = f"{name}_{timestamp}.xlsx"
    export_path = os.path.join(export_to or os.getcwd(), export_filename)
    df.to_excel(export_path, index=False)
    return f"成功匯出 {name}.xlsx 為 {export_filename}"