# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serial_ports_qt_gui2.ui'
#
# Created: Mon Oct 06 20:42:30 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!
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

class Ui_Form(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        dispatcher.connect(self.add_ports, signal="PortChange", 
                            sender=dispatcher.Any)
        self.monitor = MonitorThread()
        self.monitor.setDaemon(True)
        self.monitor.start()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(230, 316)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        QtGui.QListWidgetItem(self.listWidget)
        self.horizontalLayout.addWidget(self.listWidget)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Serial Ports", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.item(0).setText(QtGui.QApplication.translate("Form", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        
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
        self.listWidget.clear()
        for item in self.port_list:
            self.listWidget.addItem(item)
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
    ex = Ui_Form()
    ex.show()
    sys.exit(app.exec_())