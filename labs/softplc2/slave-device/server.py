#!/usr/bin/env python
"""
Based on Modbus Synchronous Server Example
--------------------------------------------------------------------------

Manage a simple board with a switch and a light bulb, each of which
are rendered using QT.  
"""
# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
from pymodbus.server.sync import StartTcpServer
from pymodbus.server.sync import StartUdpServer
from pymodbus.server.sync import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from pymodbus.transaction import ModbusRtuFramer, ModbusBinaryFramer
#from twisted.internet.task import LoopingCall
from threading import Thread
import time
import signal, sys
from PySide2.QtWidgets import QApplication, QPushButton, QLabel, QWidget, QVBoxLayout
# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(filename='/tmp/server.log', format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

READ_COIL = 1
READ_INPUT = 2

class GUI(Thread):
    ''' render the board items and write descrete inputs when button is pushed. '''
    die = False
    def __init__(self, context):
        Thread.__init__(self)
        self.app = None
        self.bulb = None
        self.context = context[0]
     
    def clickedButton1(self):
        log.info('clicked')
        ''' descrete input function seems to be 2 '''
        address = 0x00
        old_values = self.context.getValues(READ_INPUT, address, count=1)
        log.info('old values: ' + str(old_values))
        values = [1 for v in old_values]
        log.info('clickedButton1 reg 2 addr 0 new values: ' + str(values))
        self.context.setValues(READ_INPUT, address, values)
        time.sleep(1)
        self.context.setValues(READ_INPUT, address, old_values)

    def clickedButton2(self):
        log.info('clicked')
        ''' descrete input function seems to be 2 '''
        address = 0x01
        old_values = self.context.getValues(READ_INPUT, address)
        log.info('old values: ' + str(old_values))
        values = [1 for v in old_values]
        log.info('clickedButton2 reg %d addr 0x%x new values: %s' % (READ_INPUT, address, str(values)))
        self.context.setValues(READ_INPUT, address, values)
        time.sleep(1)
        self.context.setValues(READ_INPUT, address, old_values)
 
    def run(self):
        self.app = QApplication(sys.argv)
        win = QWidget()
        vbox = QVBoxLayout()
        button1 = QPushButton('Button 1')
        button2 = QPushButton('Button 2')
        button1.clicked.connect(self.clickedButton1)
        button2.clicked.connect(self.clickedButton2)
        self.bulb = QLabel()
        self.bulb.setText("Bulb: OFF")
        vbox.addWidget(button1)
        vbox.addWidget(button2)
        vbox.addWidget(self.bulb)
        win.setLayout(vbox)
        win.setWindowTitle('Physical Board')
        win.resize(200,200)
        win.show()
        try:
            self.app.exec_()
        except KeyboardInterrupt:
            log.info('GUI FOUND interrupt')
            self.endMe()

    def setBulb(self, is_on):
        if self.bulb is not None:
            if is_on:
                self.bulb.setText("Bulb: ON")
                self.bulb.setStyleSheet('background-color: yellow')
            else:
                self.bulb.setText("Bulb: OFF")
                self.bulb.setStyleSheet('background-color: white')

    def endMe(self):
        self.app.exit()
        exit(0) 

class PollCoil(Thread):
    ''' read coil values from the PLC and set the bulb accordingly '''
    die = False
    def __init__(self, a, gui):
        Thread.__init__(self)
        self.context = a[0]
        self.gui = gui
        self.prev_value = None

    def checkCoil(self):
        ''' read the coil value and update bulb if it has changed '''
        myvalues = self.context.getValues(READ_COIL, 0)
        if self.prev_value is None or self.prev_value != myvalues[0]:
            log.info('checkCoil getValues(%d, 0) : %s' % (READ_COIL, str(myvalues)))
            try:
                self.gui.setBulb(myvalues[0])
            except:
                self.endMe()
            self.prev_value = myvalues[0]

    def run(self):
        try:
            while not self.die:
                self.checkCoil()
                time.sleep(0.5)
            log.info('leaving thread')
        except KeyboardInterrupt:
            log.info('PollCoil got keyboard interrupt')
            self.endMe()

    def endMe(self):
        self.die = True
        self.gui.endMe()
        exit(0)
        
    
def run_server():
    # ----------------------------------------------------------------------- #
    # initialize your data store
    # ----------------------------------------------------------------------- #
    # The datastores only respond to the addresses that they are initialized to
    # Therefore, if you initialize a DataBlock to addresses of 0x00 to 0xFF, a
    # request to 0x100 will respond with an invalid address exception. This is
    # because many devices exhibit this kind of behavior (but not all)::
    #
    #     block = ModbusSequentialDataBlock(0x00, [0]*0xff)
    #
    # Continuing, you can choose to use a sequential or a sparse DataBlock in
    # your data context.  The difference is that the sequential has no gaps in
    # the data while the sparse can. Once again, there are devices that exhibit
    # both forms of behavior::
    #
    #     block = ModbusSparseDataBlock({0x00: 0, 0x05: 1})
    #     block = ModbusSequentialDataBlock(0x00, [0]*5)
    #
    # Alternately, you can use the factory methods to initialize the DataBlocks
    # or simply do not pass them to have them initialized to 0x00 on the full
    # address range::
    #
    #     store = ModbusSlaveContext(di = ModbusSequentialDataBlock.create())
    #     store = ModbusSlaveContext()
    #
    # Finally, you are allowed to use the same DataBlock reference for every
    # table or you may use a separate DataBlock for each table.
    # This depends if you would like functions to be able to access and modify
    # the same data or not::
    #
    #     block = ModbusSequentialDataBlock(0x00, [0]*0xff)
    #     store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
    #
    # The server then makes use of a server context that allows the server to
    # respond with different slave contexts for different unit ids. By default
    # it will return the same context for every unit id supplied (broadcast
    # mode).
    # However, this can be overloaded by setting the single flag to False and
    # then supplying a dictionary of unit id to context mapping::
    #
    #     slaves  = {
    #         0x01: ModbusSlaveContext(...),
    #         0x02: ModbusSlaveContext(...),
    #         0x03: ModbusSlaveContext(...),
    #     }
    #     context = ModbusServerContext(slaves=slaves, single=False)
    #
    # The slave context can also be initialized in zero_mode which means that a
    # request to address(0-7) will map to the address (0-7). The default is
    # False which is based on section 4.4 of the specification, so address(0-7)
    # will map to (1-8)::
    #
    #     store = ModbusSlaveContext(..., zero_mode=True)
    # ----------------------------------------------------------------------- #
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),
        co=ModbusSequentialDataBlock(0, [0]*100),
        hr=ModbusSequentialDataBlock(0, [0]*100),
        ir=ModbusSequentialDataBlock(0, [0]*100))

    context = ModbusServerContext(slaves=store, single=True)

    # ----------------------------------------------------------------------- #
    # initialize the server information
    # ----------------------------------------------------------------------- #
    # If you don't set this or any fields, they are defaulted to empty strings.
    # ----------------------------------------------------------------------- #
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '2.2.0'

    # ----------------------------------------------------------------------- #
    # run the server you want
    # ----------------------------------------------------------------------- #
    # Tcp:
    stop_thread = False
    ''' create board representation ''' 
    gui_thread = GUI(context)
    gui_thread.start()
    ''' thread to poll coil status '''
    thread = PollCoil(context, gui_thread)
    thread.start()
    log.info('now start')
    try:
        StartTcpServer(context, identity=identity, address=("0.0.0.0", 502))
    except KeyboardInterrupt:
        log.info('FOUND interrupt')
        thread.endMe()
        gui_thread.endMe()
        thread.join()
        gui_thread.join()
        exit(0)
 

    # TCP with different framer
    # StartTcpServer(context, identity=identity,
    #                framer=ModbusRtuFramer, address=("0.0.0.0", 5020))

    # Udp:
    # StartUdpServer(context, identity=identity, address=("0.0.0.0", 5020))

    # Ascii:
    # StartSerialServer(context, identity=identity,
    #                    port='/dev/ttyp0', timeout=1)

    # RTU:
    # StartSerialServer(context, framer=ModbusRtuFramer, identity=identity,
    #                   port='/dev/ttyp0', timeout=.005, baudrate=9600)

    # Binary
    # StartSerialServer(context,
    #                   identity=identity,
    #                   framer=ModbusBinaryFramer,
    #                   port='/dev/ttyp0',
    #                   timeout=1)


if __name__ == "__main__":
    run_server()

