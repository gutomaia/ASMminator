import wx, sys, os
import wx.grid
from collections import OrderedDict
from gameengine import DisplayScene


class VarGrid(wx.grid.Grid):

    _vars = ['A', 'X', 'Y', 'P', 'SP', 'PC']

    def __init__(self, parent):
        super(VarGrid, self).__init__(parent, -1)
        self.CreateGrid(len(self._vars), 3)
        self.parent = parent
        self.update()

    def update(self):
        scene = self.parent.display.active_scene
        self.SetColLabelValue(0, 'Hex')
        self.SetColLabelValue(1, 'Dec')
        self.SetColLabelValue(2, 'Bin')

        for index, var in enumerate(self._vars):
            value = scene.cpu_register(var)
            self.SetRowLabelValue(index, var)
            self.SetCellValue(index, 0, '0x%0.2X' % value)
            self.SetCellValue(index, 1, '%s' % value)
            self.SetCellValue(index, 2, '{0:08b}'.format(value))


class Frame(wx.Frame):

    def init_menubar(self):
        self.menubar = wx.MenuBar()

        menus = OrderedDict()
        menus['&File'] = wx.Menu()
        menus['&Run'] = wx.Menu()
        menus['&Help'] = wx.Menu()

        for command in self.commands.values():
            if command._menu and command._menu[0] in menus.keys():
                command.attach(menus[command._menu[0]], self)

        for label, menu in menus.iteritems():
            self.menubar.Append(menu, label)

        self.SetMenuBar(self.menubar)
        self.Bind(wx.EVT_MENU, self.menuhandler)

    def menuhandler(self, event):
        menu_id = event.GetId()
        if menu_id == wx.ID_EXIT:
            self.Kill(event)

    def init_toolbar(self):
        # self.toolbar = self.CreateToolBar(wx.TB_TEXT, wx.TB_NOICONS, -1)
        self.toolbar = self.CreateToolBar()
        for command in self.commands.values():
            if command._toolbar:
                command.attach(self.toolbar, self)
        self.toolbar.Realize()

    def run_command(self, event):
        source = self.editor.GetText()
        self.display.active_scene.input_code(source)

    def init_statusbar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-3, -4, -2])
        self.statusbar.SetStatusText("ASMminator", 0)
        self.statusbar.SetStatusText("Look, it's a nifty status bar!!!", 1)

    def __init__(self, parent, starting_scene):
        wx.Frame.__init__(self, parent, -1, size = (600, 600))
        self.SetTitle("ASMminator")

        from commands import commands
        self.commands = OrderedDict()
        for label, Command in commands.iteritems():
            self.commands[label] = Command(self)

        self.init_menubar()
        self.init_toolbar()
        self.init_statusbar()

        self.display = DisplayScene(self, starting_scene)

        self.Bind(wx.EVT_CLOSE, self.Kill)

        self.timer = wx.Timer(self)

        self.Bind(wx.EVT_SCROLL, self.OnScroll)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)

        self.timer.Start((1000.0 / self.display.fps))

        from editor import SourceEditor
        self.editor = SourceEditor(self)
        self.vargrid = VarGrid(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.display, 1, flag = wx.EXPAND)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.sizer2, 1, wx.ALL|wx.EXPAND)



        self.sizer2.Add(self.editor, 1, flag = wx.EXPAND)
        self.sizer2.Add(self.vargrid, 1, flag = wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)
        self.Layout()

    def Kill(self, event):
        self.display.Kill(event)
        self.Destroy()

    def OnSize(self, event):
        self.Layout()

    def Update(self, event):
        pass
        # self.statusbar.SetStatusText("Frame %i" % self.curframe, 2)

    def OnScroll(self, event):
        self.display.linespacing = self.slider.GetValue()
