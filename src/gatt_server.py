import dbus

from ble_gatt_server.advertisement import Advertisement
from ble_gatt_server.service import Application, Service, Characteristic, Descriptor

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

CHESSBOARD_SVC_UUID = "00000001-502e-4e1d-b821-ae2488aa4202"

BOARDSTATE_CHRC_UUID = "00000002-502e-4e1d-b821-ae2488aa4202" # read, notify
STARTGAME_CHRC_UUID = "00000003-502e-4e1d-b821-ae2488aa4202" # write
UPDATESETTINGS_CHRC_UUID = "00000004-502e-4e1d-b821-ae2488aa4202" # read, write

class ChessboardAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("MagicChessboard")
        self.include_tx_power = True

class ChessboardService(Service):
    def __init__(self, index):
        Service.__init__(self, index, CHESSBOARD_SVC_UUID, True)
        self.add_characteristic(BoardStateCharacteristic(self))



class BoardStateCharacteristic(Characteristic):
    def __init__(self, service):
        self.notifying = False

        Characteristic.__init__(
                self, self.TEMP_CHARACTERISTIC_UUID,
                ["notify", "read"], service)
        self.add_descriptor(TempDescriptor(self))

    def get_temperature(self):
        value = []
        unit = "C"

        cpu = CPUTemperature()
        temp = cpu.temperature
        if self.service.is_farenheit():
            temp = (temp * 1.8) + 32
            unit = "F"

        strtemp = str(round(temp, 1)) + " " + unit
        for c in strtemp:
            value.append(dbus.Byte(c.encode()))

        return value

    def set_temperature_callback(self):
        if self.notifying:
            value = self.get_temperature()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_temperature()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_temperature_callback)

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_temperature()

        return value