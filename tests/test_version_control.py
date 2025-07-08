import unittest
import os
from modules import version_control

class TestVersionControl(unittest.TestCase):
    def setUp(self):
        self.message = 'Test log entry'
        if os.path.exists(version_control.VERSION_LOG_PATH):
            os.remove(version_control.VERSION_LOG_PATH)

    def test_append_log(self):
        version_control.append_version_log(self.message)
        with open(version_control.VERSION_LOG_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn(self.message, content)

if __name__ == '__main__':
    unittest.main()
