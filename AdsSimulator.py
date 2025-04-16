# see also: https://pypi.org/project/pyads/
#
import time
from tango import AttrQuality, AttrWriteType, DispLevel, DevState, Attr, CmdArgType, UserDefaultAttrProp, Util
from tango.server import Device, attribute, command, DeviceMeta
from tango.server import class_property, device_property
from tango.server import run
import os
import json
from threading import Thread
from threading import Lock
import datetime
from pyads.testserver import AdsTestServer, BasicHandler, AdvancedHandler, PLCVariable
from pyads import constants
import re
from json import JSONDecodeError

class AdsSimulator(Device, metaclass=DeviceMeta):
    pass
    host = device_property(dtype=str, default_value="127.0.0.1")
    port = device_property(dtype=int, default_value=48898)
    simulator_server = 0

    @attribute
    def time(self):
        return time.time()

    def runServer(self):
        self.simulator_server.start()
        self.simulator_server.join()

    def init_device(self):
        self.set_state(DevState.INIT)
        self.get_device_properties(self.get_device_class())
        h = AdvancedHandler()
        h.add_variable(PLCVariable("Main.double",bytes(8),ads_type=constants.ADST_REAL64,symbol_type="LREAL"))
        h.add_variable(PLCVariable("Main.float",bytes(4),ads_type=constants.ADST_REAL32,symbol_type="REAL"))
        h.add_variable(PLCVariable("Main.long",bytes(8),ads_type=constants.ADST_INT64,symbol_type="INT"))
        h.add_variable(PLCVariable("Main.bool",bytes(1),ads_type=constants.ADST_BIT,symbol_type="INT"))
        h.add_variable(PLCVariable("Main.string",bytes(1024),ads_type=constants.ADST_STRING,symbol_type="STRING"))
        self.simulator_server = AdsTestServer(handler=h, logging=False, ip_address=self.host, port=self.port)
        Thread(target=self.runServer, daemon=True).start()
        print("test server started on " + self.host + ":" + str(self.port) + "...")
        self.set_state(DevState.ON)

if __name__ == "__main__":
    deviceServerName = os.getenv("DEVICE_SERVER_NAME")
    run({deviceServerName: AdsSimulator})
