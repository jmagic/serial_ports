import sys
import serial_ports_qt_gui2
from PySide import QtCore, QtGui
import time
import os
import serial 
from threading import Thread
from pydispatch import dispatcher



class MonitorThread(Thread):

    #----------------------------------------------------------------------
    def __init__(self):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        #self.start()    # start the thread
 
    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        ports_old = []
        while True:
            ports = []
            for item in self.serial_ports():
                ports.append(item)
            if ports != ports_old:
                self.updateStatus, ports
                ports_old = ports
            time.sleep(5)
            print '.'

    #----------------------------------------------------------------------
    def serial_ports(self):
        """
        Returns a generator for all available serial ports
        """
        if os.name == 'nt':
            # windows
            for i in range(256):
                try:
                    my_serial = serial.Serial(i)
                    my_serial.close()
                    yield 'COM' + str(i + 1)
                except serial.SerialException:
                    pass


    def updateStatus(self, data):
        """
        Send status to GUI
        """
        dispatcher.send(signal="PortChange", sender=data)

########################################################################
class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui =  Ui_MainWindow()
        self.ui.setupUi(self)

        self.port_list = []
        self.gui_port_text = []

        #self.tbIcon = CustomTaskBarIcon(self)
        dispatcher.connect(self.add_ports, signal="PortChange", 
                            sender=dispatcher.Any)

        self.monitor = MonitorThread()
        self.monitor.setDaemon(True)
        self.monitor.start()

        #----------------------------------------------------------------------
    def on_left_click(self, event):
        """left click"""
        self.onClose(None)

    def add_ports(self, sender):
        """ add the ports to the gui """
        self.port_list = []
        for port in sender:
            if port not in self.port_list:
                self.port_list.append(port)
        self.update_gui()
        print sender

    def update_gui(self):
        #for item in self.gui_port_text:
        #    item.Destroy()
        #self.gui_port_text = []
        #for item in self.port_list:
        #    staticText = wx.StaticText(self.m_panel3, wx.ID_ANY, 
        #        str(item), wx.DefaultPosition, wx.DefaultSize, 0)
        #    staticText.Wrap(-1)
        #    self.portSizer.Add(staticText, 0, 
        #        wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        #    self.gui_port_text.append(staticText)
        #self.Layout()
        #self.Fit()
        None

    def onClose(self, evt):
        """
        Destroy the taskbar icon and the frame
        """
        #self.monitor.Exit()
        self.Destroy()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())