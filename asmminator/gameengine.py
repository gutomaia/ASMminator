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


class AsmScene(Py65CPUBridge, SceneBase):

    def __init__(self):
        self.next = self
        self.cpu = MPU()
        self.start_addr = 0
        self.stop_addr = 0

    def input_code(self, source):
        addr = 0
        self.start_addr = 0xC000
        opcodes = assembly(source, self.start_addr)
        self.cpu_pc(self.start_addr)
        for addr, val in enumerate(opcodes, start=self.start_addr):
            self.memory_set(addr, val)
        self.stop_addr = addr

    def update(self, deltaTime):
        if self.cpu.pc < self.stop_addr:
            self.execute()


class Level1(AsmScene):

    def __init__(self):
        super(Level1, self).__init__()
        self.position = [100, 100]

    def update(self, deltaTime):
        super(Level1, self).update(deltaTime)
        if self.memory_fetch(0x0010) == 0x0001:
            self.position[0] += 1
            self.memory_set(0x0010, 0x00)

    def render(self, screen):
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (0, 255, 0), self.position, 5)



class DisplayScene(PygameDisplay):

    def __init__(self, parent, ID, starting_scene=None):
        super(DisplayScene, self).__init__(parent, ID)

        if not starting_scene:
            self.active_scene = Level1()
        else:
            self.active_scene = starting_scene

    def pygame_redraw(self, deltaTime):
        self.active_scene.update(deltaTime)
        self.active_scene.render(self.screen)
        self.active_scene = self.active_scene.next
