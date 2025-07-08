import unittest
from unittest.mock import MagicMock, patch
from modules.plc_interface import PLCInterface

class TestPLCInterface(unittest.TestCase):
    @patch('modules.plc_interface.win32com.client.Dispatch')
    def test_read_write_device(self, mock_dispatch):
        # 模擬成功讀寫
        mock_instance = mock_dispatch.return_value
        mock_instance.ReadDeviceBlock2.return_value = (0, [123])
        mock_instance.WriteDeviceBlock2.return_value = 0  # ← 這裡是關鍵

        plc = PLCInterface()
        values = plc.read_device('D100', count=1)
        self.assertEqual(values, [123])

        # 測試寫入（不應該觸發 Exception）
        plc.write_device('D100', [321])

if __name__ == '__main__':
    unittest.main()
