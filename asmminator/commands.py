import wx
from collections import OrderedDict
from nesasm.compiler import lexical, semantic, syntax, Cartridge


class Command(object):
    _icon = None
    _icon_image = None
    _label = 'command'
    _toolbar = False
    _menu = None

    def __init__(self, ui):
        self.ui = ui

    @property
    def icon(self):
        if not self._icon:
            self._icon = wx.Bitmap(self._icon_image)
        return self._icon

    def execute(self, event):
        pass

    def attach(self, element, ui):
        if isinstance(element, wx.ToolBar):
            tool = element.AddLabelTool(wx.ID_ANY, self._label, self.icon)
            ui.Bind(wx.EVT_TOOL, self.execute, tool)
        elif isinstance(element, wx.Menu):
            menuitem = wx.MenuItem(element, self._menu_id, self._menu_label)
            element.AppendItem(menuitem)


class Quit(Command):
    _label = 'Quit'
    _toolbar = False
    _menu = ('&File', 1)
    _menu_id = wx.ID_EXIT
    _menu_label = '&Quit\tCtrl+Q'

    def execute(self, event):
        self.ui.Kill(event)


class About(Command):
    _label = 'About'
    _toolbar = False
    _menu = ('&Help', 0)
    _menu_id = 12753
    _menu_label = 'About'


class Compile(Command):
    _label = 'Compile'
    _toolbar = False

    def execute(self, event):
        source = self.ui.editor.GetText()
        start_addr = 0xC000
        cart = Cartridge()
        if start_addr != 0:
            cart.set_org(start_addr)
            opcodes = semantic(syntax(lexical(source)), False, cart)
            self.ui.display.active_scene.input_opcodes(opcodes, 0xC000)


class Run(Command):
    _label = 'Run'
    _icon_image = 'assets/icons/play.png'
    _toolbar = True
    _menu = ('&Run', 1)
    _menu_id = 12754
    _menu_label = '&Run\tCtrl+R'


    def execute(self, event):
        self.ui.display.active_scene.paused = False
        self.ui.display.active_scene.step = False
        self.ui.commands['compile'].execute(event)


class Pause(Command):
    _label = 'Pause'
    _icon_image = 'assets/icons/pause.png'
    _toolbar = True
    _menu = ('&Run', 1)
    _menu_id = 12754
    _menu_label = 'Pause'


    def execute(self, event):
        self.ui.display.active_scene.paused = not self.ui.display.active_scene.paused


class Step(Command):
    _label = 'Step'
    _icon_image = 'assets/icons/step_forward.png'
    _toolbar = True
    _menu = ('&Run', 1)
    _menu_id = 12755
    _menu_label = 'Step'

    def execute(self, event):
        self.ui.display.active_scene.paused = True
        self.ui.display.active_scene.step = True


commands = OrderedDict()
commands['Quit'] = Quit
commands['About'] = About
commands['compile'] = Compile
commands['run'] = Run
commands['pause'] = Pause
commands['step'] = Step
