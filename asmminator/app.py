import wx
from ui import Frame


class App(wx.App):
    def OnInit(self):
        self.frame = Frame(parent = None)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)

        return True

if __name__ == "__main__":
    app = App()
    app.MainLoop()
