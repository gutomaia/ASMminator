from ui import PygameDisplay
import pygame
from nesasm.compiler import lexical, semantic, syntax, Cartridge
from bridge import Py65CPUBridge
from py65.devices.mpu6502 import MPU


def assembly(source, start_addr=0):
    cart = Cartridge()
    if start_addr != 0:
      cart.set_org(start_addr)
    return semantic(syntax(lexical(source)), False, cart)


class SceneBase(object):

    def __init__(self):
        self.next = self

    def input_code(self, source):
        pass

    def update(self, deltaTime):
        pass

    def render(self, screen):
        pass

    def go_to_scene(self, next_scene):
        self.next = next_scene

    def terminate(self):
        self.go_to_scene(None)


class MemoryInterface(object):
    pass


class AsmScene(Py65CPUBridge, SceneBase):

    def __init__(self):
        self.next = self
        self.cpu = MPU()
        self.start_addr = 0xC000
        self.stop_addr = 0xC000

    def input_code(self, source):
        opcodes = assembly(source, self.start_addr)
        self.cpu_pc(self.start_addr)
        for addr, val in enumerate(opcodes, start=self.start_addr):
            self.memory_set(addr, val)
        self.stop_addr = addr

    def update(self, deltaTime):
        if self.cpu.pc < self.stop_addr:
            self.execute()


class DisplayScene(PygameDisplay):

    def __init__(self, parent, ID, starting_scene=None):
        super(DisplayScene, self).__init__(parent, ID)
        import sys
        # pygame.init()


        if not starting_scene:
            self.active_scene = AsmScene()
        else:
            self.active_scene = starting_scene

    def pygame_redraw(self, deltaTime):
        self.active_scene.update(deltaTime)
        self.active_scene.render(self.screen)
        self.active_scene = self.active_scene.next
