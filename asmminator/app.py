import wx
from ui import Frame
from levels import Level1

class App(wx.App):
    def OnInit(self):
        self.frame = Frame(None, Level1())
        self.frame.Show(True)
        self.SetTopWindow(self.frame)

        return True

if __name__ == "__main__":
    app = App()
    app.MainLoop()
