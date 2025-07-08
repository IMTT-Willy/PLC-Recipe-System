
import win32com.client

class PLC:
    def __init__(self, station=1):
        self.station = station
        self.act = win32com.client.Dispatch("ActUtlType.ActUtlType.1")
        self.act.ActLogicalStationNumber = self.station
        self.connected = False

    def open(self):
        result = self.act.Open()
        self.connected = (result == 0)
        if not self.connected:
            raise ConnectionError(f"Failed to connect to PLC (Station {self.station}), error code: {result}")

    def close(self):
        if self.connected:
            self.act.Close()
            self.connected = False

    def write(self, device, value):
        if not self.connected:
            raise RuntimeError("PLC not connected. Call open() first.")
        result = self.act.SetDevice(device, int(value))
        if result != 0:
            raise ValueError(f"Failed to write to {device}, error code: {result}")

    def read(self, device):
        if not self.connected:
            raise RuntimeError("PLC not connected. Call open() first.")
        value = self.act.GetDevice(device, 0)
        return value
