import win32com.client
import pandas as pd

class PLCInterface:
    def __init__(self, logical_station_number: int = 1):
        self.plc = win32com.client.Dispatch("ActUtlType.ActUtlType.1")
        self.plc.ActLogicalStationNumber = logical_station_number
        self.plc.Open()

    def read_device(self, device: str, count: int = 1) -> list[int]:
        values = [0] * count
        result = self.plc.ReadDeviceBlock2(device, count, values)
        if result != 0:
            raise Exception(f"讀取 {device} 時發生錯誤，錯誤碼: {result}")
        return values

    def write_device(self, devices: list, values: list) -> None:
        print(f"[DEBUG] 傳入 PLC 的位址: {devices}")
        print(f"[DEBUG] 傳入 PLC 的值: {values} (type: {type(values)} / 元素型別: {[type(v) for v in values]})")

        def flatten_and_cast(lst):
            flat = []
            for item in lst:
                while isinstance(item, list):
                    if not item:
                        raise ValueError("空 list 無法轉換")
                    item = item[0]
                if hasattr(item, 'item'):
                    item = item.item()
                flat.append(int(item))
            return flat

        clean_values = flatten_and_cast(values)
        clean_values = [int(x) for x in clean_values]

        print(f"[DEBUG] 寫入 PLC 的最終值: {clean_values}")

        if len(devices) != len(clean_values):
            raise ValueError("地址數量與數值數量不符")

        for device, value in zip(devices, clean_values):
            result = self.plc.SetDevice(device, value)
            if result != 0:
                raise Exception(f"寫入 {device} 時發生錯誤，錯誤碼: {result}")
            else:
                print(f"✔️ 寫入 {device} 成功：{value}")

    def close(self):
        self.plc.Close()

if __name__ == "__main__":
    # 測試程式入口點（僅供手動執行）
    plc = PLCInterface()
    df = pd.read_excel("Sheet1.xlsx")  # 確保這個檔案存在且格式正確
    address_list = df['Address'].tolist()
    value_list = df['Value'].tolist()
    plc.write_device(address_list, value_list)
    plc.close()
