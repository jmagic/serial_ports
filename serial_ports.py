import sys
from PySide import QtGui
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
                self.updateStatus(ports)
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


class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        


        self.port_list = []
        self.gui_port_text = []

        #self.tbIcon = CustomTaskBarIcon(self)
        dispatcher.connect(self.add_ports, signal="PortChange", 
                            sender=dispatcher.Any)
        
        self.monitor = MonitorThread()
        self.monitor.setDaemon(True)
        self.monitor.start()
        self.setToolTip('None')
        print self.supportsMessages()
        self.showMessage('Hello', 'Test')


    def add_ports(self, sender):
        """ add the ports to the gui """
        self.port_list = []
        for port in sender:
            if port not in self.port_list:
                self.port_list.append(port)
        popup_text = ''
        for item in self.port_list:
            popup_text = popup_text + item + '\n'
        self.setToolTip(popup_text)
        self.showMessage('Port Change Detected', popup_text)


    def update_gui(self):
        for item in self.gui_port_text:
            item.Destroy()
        self.gui_port_text = []
        for item in self.port_list:
            self.gui_port_text.append(item)
        self.setToolTip(self.gui_port_text)


    def onClose(self, evt):
        """
        Destroy the taskbar icon and the frame
        """
        #self.monitor.Exit()
        self.Destroy()



def main():
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("dsub2.png"), w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()