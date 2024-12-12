from machine import I2C
import struct

# Constants
MAX1704X_I2CADDR_DEFAULT = 0x36
_MAX1704X_VCELL_REG = 0x02
_MAX1704X_SOC_REG = 0x04
_MAX1704X_MODE_REG = 0x06
_MAX1704X_VERSION_REG = 0x08
_MAX1704X_CMD_REG = 0xFE

class MAX17048:
    def __init__(self, i2c: I2C, address: int = MAX1704X_I2CADDR_DEFAULT):
        self.i2c = i2c
        self.address = address
        
        print("chip version: ")
        print(self.get_chip_version())
        
        if self.get_chip_version() & 0xFFF0 != 0x0010:
            raise RuntimeError("Failed to find MAX1704X - check your wiring!")
        #self.reset()

    def read_register(self, register: int, length: int = 2) -> bytes:
        """Read bytes from the specified register."""
        self.i2c.writeto(self.address, bytes([register]))
        return self.i2c.readfrom(self.address, length)

    def write_register(self, register: int, data: bytes) -> None:
        """Write bytes to the specified register."""
        self.i2c.writeto(self.address, bytes([register]) + data)

    def get_chip_version(self) -> int:
        """Get the chip version."""
        raw = self.read_register(_MAX1704X_VERSION_REG)
        return struct.unpack(">H", raw)[0]


    def get_cell_voltage(self) -> float:
        """Get the cell voltage in volts."""
        raw = self.read_register(_MAX1704X_VCELL_REG)
        voltage = struct.unpack(">H", raw)[0]
        return voltage * 78.125 / 1_000_000

    def get_cell_percent(self) -> float:
        """Get the state of charge in percentage."""
        raw = self.read_register(_MAX1704X_SOC_REG)
        soc = struct.unpack(">H", raw)[0]
        return soc / 256.0


