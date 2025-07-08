import unittest
import os
import pandas as pd
from modules import autosave

class TestAutosave(unittest.TestCase):
    def setUp(self):
        self.category = 'test_category'
        self.name = 'test_file'
        self.path = os.path.join('recipes', self.category)
        os.makedirs(self.path, exist_ok=True)
        self.df = pd.DataFrame({'A': [1]})
        self.df.to_excel(os.path.join(self.path, self.name + '.xlsx'), index=False)

    def tearDown(self):
        import shutil
        shutil.rmtree('recipes/test_category', ignore_errors=True)
        shutil.rmtree('backup/test_category', ignore_errors=True)

    def test_autosave(self):
        msg = autosave.autosave_recipe(self.category, self.name)
        self.assertIn('已自動備份', msg)

if __name__ == '__main__':
    unittest.main()
