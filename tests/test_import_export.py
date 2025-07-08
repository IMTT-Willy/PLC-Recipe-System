import unittest
import os
import pandas as pd
from modules import import_export

class TestImportExport(unittest.TestCase):
    def setUp(self):
        self.temp_file = 'test_recipe.xlsx'
        self.df = pd.DataFrame({'A': [1], 'B': [2]})
        self.df.to_excel(self.temp_file, index=False)
        self.required_columns = ['A', 'B']

    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_validate_format_pass(self):
        self.assertTrue(import_export.validate_recipe_format(self.df, self.required_columns))

    def test_validate_format_fail(self):
        self.assertFalse(import_export.validate_recipe_format(self.df, ['X', 'Y']))

if __name__ == '__main__':
    unittest.main()
