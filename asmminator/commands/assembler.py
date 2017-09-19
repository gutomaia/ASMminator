from nesasm.compiler import lexical, semantic, syntax, Cartridge


def assembly(source, start_addr=0):
    cart = Cartridge()
    if start_addr != 0:
      cart.set_org(start_addr)
    return semantic(syntax(lexical(source)), False, cart)

def load_program(code):
    start_addr = 0x0100
    opcodes = assembly(code, start_addr)


def run_program():
    b = 0
    while self.cpu.pc < self.stop_addr:
        self.execute()
        if b > 1000:
            raise Exception('dammit')
            break
        b += 1


def run_command(self, event):
    source = self.editor.GetText()
    context = {}
    try:
        compiled = compile(source, '<string>', 'exec')
        exec(compiled, context)
    except SyntaxError, e:
        print 'syntax error'
    except Exception, e:

        # TODO
        # print e
        pass

    print context
    print 'ok'
