import wx


class Command(object):
    _icon = None
    _icon_image = None
    _label = 'command'

    @property
    def icon(self):
        if not self._icon:
            self._icon = wx.Bitmap(self._icon_image)
        return self._icon

    def execute(self, event):
        pass

    def attach(self, toolbar, ui):
        command = toolbar.AddLabelTool(wx.ID_ANY, self._label, self.icon)
        ui.Bind(wx.EVT_TOOL, self.execute, command)


class Run(Command):
    _label = 'Run'
    _icon_image = 'assets/icons/play.png'

    def __init__(self, ui):
        self.ui = ui

    def execute(self, event):
        self.ui.display.active_scene.paused = False
        self.ui.display.active_scene.step = False
        source = self.ui.editor.GetText()
        self.ui.display.active_scene.input_code(source)


class Pause(Command):
    _label = 'Pause'
    _icon_image = 'assets/icons/pause.png'

    def __init__(self, ui):
        self.ui = ui

    def execute(self, event):
        self.ui.display.active_scene.paused = not self.ui.display.active_scene.paused


class Step(Command):
    _label = 'Step'
    _icon_image = 'assets/icons/step_forward.png'

    def __init__(self, ui):
        self.ui = ui

    def execute(self, event):
        self.ui.display.active_scene.paused = True
        self.ui.display.active_scene.step = True


commands = {}
commands['run'] = Run
commands['pause'] = Pause
commands['step'] = Step
