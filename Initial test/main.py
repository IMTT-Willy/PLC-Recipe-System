from plc import PLC
from excel_io import load_recipe

def main():
    filepath = "../Recipe_System/recipes/board_parameters/board_template.xlsx"  # 修改為你的測試路徑
    recipe = load_recipe(filepath)

    plc = PLC(station=1)
    try:
        plc.open()
        for addr, val in recipe:
            plc.write(addr, val)
            print(f"Wrote {val} to {addr}")
    finally:
        plc.close()

if __name__ == "__main__":
    main()