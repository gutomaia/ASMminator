import wx
import wx.stc as stc

STYLE_DEFAULT, STYLE_INSTRUCTION = range(2)


class SourceEditor(stc.StyledTextCtrl):
    def __init__(self, parent, style=wx.SIMPLE_BORDER):
        super(SourceEditor, self).__init__(parent, style=style)
        self.SetUseTabs(False)
        self.SetTabWidth(4)

        self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.SetMarginType(2, wx.stc.STC_MASK_FOLDERS)

        self.SetLexer(stc.STC_LEX_CONTAINER)
        self.StyleSetSpec(STYLE_DEFAULT, 'fore:#0000FF,back:#FFFFFF')
        self.StyleSetSpec(STYLE_INSTRUCTION, 'fore:#FF0000,bold')

        self.Bind(stc.EVT_STC_STYLENEEDED, self.OnStyle)

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

    def __init__(self):
        super(ASMLexter, self).__init__()
        self._kw = ('ADC|AND|ASL|BCC|BCS|BEQ|BIT|BMI|BNE|BPL|BRK|BVC|BVS|CLC|'
                'CLD|CLI|CLV|CMP|CPX|CPY|DEC|DEX|DEY|EOR|INC|INX|INY|JMP|JSR|'
                'LDA|LDX|LDY|LSR|NOP|ORA|PHA|PHP|PLA|PLP|ROL|ROR|RTI|RTS|SBC|'
                'SEC|SED|SEI|STA|STX|STY|TAX|TAY|TSX|TXA|TXS|TYA').split('|')

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
                curWord = curWord.strip()

                if curWord.upper() in self._kw:
                    style = STYLE_INSTRUCTION
                else:
                    style = STYLE_DEFAULT

                wordStart = max(0, startPos - (len(curWord)))
                buff.StartStyling(wordStart, 0x1f)
                buff.SetStyling(len(curWord), style)
                buff.SetStyling(1, STYLE_DEFAULT)
                curWord = ""
            startPos += 1

