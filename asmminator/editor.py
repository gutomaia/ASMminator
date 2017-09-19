import wx
import wx.stc as stc

class SourceEditor(stc.StyledTextCtrl):
    def __init__(self, parent, style=wx.SIMPLE_BORDER):
        super(SourceEditor, self).__init__(parent, style=style)
        self.SetUseTabs(False)
        self.SetTabWidth(4)
        self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.SetMarginType(2, wx.stc.STC_MASK_FOLDERS)
        self.SetMarginWidth(2, 12)

        self.SetLexer(stc.STC_LEX_PYTHON)
        self.StyleClearAll()

        self.Bind(stc.EVT_STC_MODIFIED, self.on_text_change)
        self.Bind(stc.EVT_STC_STYLENEEDED, self.onStyleNeeded)

    def on_text_change(self, event):
        # self.onStyleNeeded(event)
        pass

    def onStyleNeeded(self, event):
        print 'ok'
        start = self.GetEndStyled()    # this is the first character that needs styling
        end = event.GetPosition()          # this is the last character that needs styling
        print start, end
        self.StartStyling(start, 31)   # in this example, only style the text style bits
        for pos in range(start, end):  # in this example, simply loop over it..
            self.SetStyling(1, 0)

