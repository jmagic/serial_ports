"""Serial Port Finder"""
import wx
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
                wx.CallAfter(self.updateStatus, ports)
                ports_old = ports
            time.sleep(5)

 
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

class MainFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title=wx.EmptyString,
         pos=wx.DefaultPosition, size=wx.Size(110, 230), style=0)
        
        
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        
        bSizer8 = wx.BoxSizer(wx.VERTICAL)
        
        self.m_panel3 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, 
            wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer9 = wx.BoxSizer(wx.VERTICAL)
        
        bSizer10 = wx.BoxSizer(wx.VERTICAL)
        
        self.m_staticText5 = wx.StaticText(self.m_panel3, wx.ID_ANY, 
            u"Serial Ports", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        bSizer10.Add(self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        
        
        bSizer9.Add(bSizer10, 0, wx.EXPAND, 5)
        
        bSizer11 = wx.BoxSizer(wx.VERTICAL)
        
        self.m_staticline2 = wx.StaticLine(self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer11.Add(self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5)
        
        
        bSizer9.Add(bSizer11, 0, wx.EXPAND, 5)
        
        self.portSizer = wx.BoxSizer(wx.VERTICAL)
        
        
        bSizer9.Add(self.portSizer, 1, wx.EXPAND, 5)
        
        
        self.m_panel3.SetSizer(bSizer9)
        self.m_panel3.Layout()
        bSizer9.Fit(self.m_panel3)
        bSizer8.Add(self.m_panel3, 1, wx.EXPAND |wx.ALL, 0)
        
        
        self.SetSizer(bSizer8)
        self.Layout()
        
        self.Centre(wx.BOTH)
        self.m_panel3.Bind(wx.EVT_LEFT_DOWN, self.on_left_click)

 
        

        self.port_list = []
        self.gui_port_text = []

        #self.tbIcon = CustomTaskBarIcon(self)
        dispatcher.connect(self.add_ports, signal="PortChange", 
                            sender=dispatcher.Any)
        
        self.monitor = MonitorThread()
        self.monitor.setDaemon(True)
        self.monitor.start()
        self.Show()
        self.Fit()

 
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





    def update_gui(self):
        for item in self.gui_port_text:
            item.Destroy()
        self.gui_port_text = []
        for item in self.port_list:
            staticText = wx.StaticText(self.m_panel3, wx.ID_ANY, 
                str(item), wx.DefaultPosition, wx.DefaultSize, 0)
            staticText.Wrap(-1)
            self.portSizer.Add(staticText, 0, 
                wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
            self.gui_port_text.append(staticText)
        self.Layout()
        self.Fit()


    def onClose(self, evt):
        """
        Destroy the taskbar icon and the frame
        """
        #self.monitor.Exit()
        self.Destroy()
 


#----------------------------------------------------------------------
def main():
    """"""
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
 
if __name__ == "__main__":
    main()