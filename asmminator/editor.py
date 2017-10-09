import wx
import wx.stc as stc
from nesasm.compiler import asm65_tokens
from re import match


STYLE_DEFAULT = 0
STYLE_INSTRUCTION = 1
STYLE_ADDRESS = 2
STYLE_HEX_NUMBER = 3
STYLE_BINARY_NUMBER = 4
STYLE_DECIMAL_NUMBER = 5
STYLE_LABEL = 6
STYLE_MARKER = 7

ANNOTATION_ERROR = 20
ANNOTATION_WARN = 21


class SourceEditor(stc.StyledTextCtrl):
    def __init__(self, parent, style=wx.SIMPLE_BORDER):
        super(SourceEditor, self).__init__(parent, style=style)
        self.SetUseTabs(False)
        self.SetTabWidth(4)

        self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.SetMarginType(2, wx.stc.STC_MASK_FOLDERS)

        self.SetLexer(stc.STC_LEX_CONTAINER)
        self.StyleSetSpec(STYLE_DEFAULT, 'fore:#000000,back:#FFFFFF')
        self.StyleSetSpec(STYLE_INSTRUCTION, 'fore:#CD2990,bold')
        self.StyleSetSpec(STYLE_ADDRESS, 'fore:#9370db')
        self.StyleSetSpec(STYLE_HEX_NUMBER, 'fore:#9370db')
        self.StyleSetSpec(STYLE_BINARY_NUMBER, 'fore:#9370db')
        self.StyleSetSpec(STYLE_DECIMAL_NUMBER, 'fore:#9370db')
        self.StyleSetSpec(STYLE_LABEL, 'fore:#00FF00,bold')
        self.StyleSetSpec(STYLE_MARKER, 'fore:#FFA500')
        self.Bind(stc.EVT_STC_STYLENEEDED, self.OnStyle)

        self.AnnotationSetVisible(stc.STC_ANNOTATION_BOXED)
        self.StyleSetSpec(ANNOTATION_ERROR, 'fore:#8B0000,bold,back:#FF967A')
        self.StyleSetSpec(ANNOTATION_WARN, 'fore:#DD6A00,bold,back:#F5DEB3')

    def set_error(self, line, message):
        self.AnnotationSetText(line, message)
        self.AnnotationSetStyle(line, ANNOTATION_ERROR)

    def set_warnning(self, line, message):
        self.AnnotationSetText(line, message)
        self.AnnotationSetStyle(line, ANNOTATION_WARN)

    def SetLexer(self, lexer_id):
        if lexer_id == stc.STC_LEX_CONTAINER:
            self._lexer = ASMLexter()
        super(SourceEditor, self).SetLexer(lexer_id)

    def OnStyle(self, event):
        if self._lexer:
            self._lexer.StyleText(event)
        else:
            event.skip()


class ASMLexter(object):


    def StyleText(self, event):
        buff = event.EventObject
        lastStyled = buff.GetEndStyled()
        startPos = buff.PositionFromLine(lastStyled)
        startPos = max(startPos, 0)
        endPos = event.GetPosition()

        curWord = ""
        while startPos < endPos:
            c = chr(buff.GetCharAt(startPos))
            curWord += c
            if c.isspace():
                style = STYLE_DEFAULT
                for i in range(7):
                    if match(asm65_tokens[i]['regex'], curWord):
                        style = i + 1
                        break

                curWord = curWord.strip()

                wordStart = max(0, startPos - (len(curWord)))
                buff.StartStyling(wordStart, 0x1f)
                buff.SetStyling(len(curWord), style)
                buff.SetStyling(1, STYLE_DEFAULT)
                curWord = ""
            startPos += 1

