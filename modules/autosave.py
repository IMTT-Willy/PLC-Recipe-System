import os
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPE_DIR = os.path.join(BASE_DIR, 'recipes')
BACKUP_DIR = os.path.join(BASE_DIR, 'backup')

def autosave_recipe(category: str, name: str) -> str:
    """
    自動將現有的 recipe 檔案備份一份至 backup/{category}，並加上時間戳記。
    """
    recipe_path = os.path.join(RECIPE_DIR, category, f"{name}.xlsx")
    backup_path = os.path.join(BACKUP_DIR, category)
    os.makedirs(backup_path, exist_ok=True)

    if not os.path.exists(recipe_path):
        raise FileNotFoundError("找不到指定的 recipe 檔案。")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    backup_file = os.path.join(backup_path, f"{name}_autosave_{timestamp}.xlsx")
    df = pd.read_excel(recipe_path)
    df.to_excel(backup_file, index=False)
    return f"已自動備份 {name}.xlsx 為 {backup_file}"