from display import PygameDisplay
import pygame
from bridge import Py65CPUBridge
from py65.devices.mpu6502 import MPU


class SceneBase(object):

    def __init__(self):
        self.next = self
        self.update_listener = []

    def input_opcodes(self, source, start_addr=0x00):
        pass

    def update(self, deltaTime):
        pass

    def add_update_listener(self, _callable):
        if _callable not in self.update_listener:
            self.update_listener.append(_callable)

    def call_update_listener(self):
        for _callable in self.update_listener:
            _callable()

    def render(self, screen):
        pass

    def go_to_scene(self, next_scene):
        self.next = next_scene

    def terminate(self):
        self.go_to_scene(None)


class AsmScene(Py65CPUBridge, SceneBase):

    def __init__(self):
        super(AsmScene, self).__init__()
        self.reset()

    def input_opcodes(self, opcodes, start_addr=0xC000):
        addr = 0
        self.start_addr = start_addr
        self.cpu_pc(self.start_addr)
        for addr, val in enumerate(opcodes, start=self.start_addr):
            self.memory_set(addr, val)
        self.stop_addr = addr + 1

    def update(self, deltaTime):
        if self.cpu.pc < self.stop_addr and (
                not self.paused or
                (self.paused and self.step)
            ):
            self.execute()
            self.call_update_listener()
            if self.step:
                self.step = False

    def reset(self):
        self.cpu = MPU()
        self.start_addr = 0
        self.stop_addr = 0
        self.paused = False
        self.step = False


class DisplayScene(PygameDisplay):

    def __init__(self, parent, starting_scene):
        super(DisplayScene, self).__init__(parent)
        self.active_scene = starting_scene

    def pygame_redraw(self, deltaTime):
        self.active_scene.update(deltaTime)
        self.active_scene.render(self.screen)
        self.active_scene = self.active_scene.next
