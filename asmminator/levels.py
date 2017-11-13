from gameengine import AsmScene
import pygame
from math import pow


class Goal(AsmScene):

    def update(self, deltaTime):
        pass

    def render(self, screen):
        screen.fill((0, 255, 0))


class Level1(AsmScene):

    def __init__(self):
        super(Level1, self).__init__()
        self.aim = [100, 100]
        self.target = [400, 100]

    def script(self):
        self.skynet_print('You need to load 42 on the acumulator\nUse the LDA instruction to do it')
        self.skynet_print('')

    def update(self, deltaTime):
        super(Level1, self).update(deltaTime)
        if self.memory_fetch(0x0010) == 0x0001:
            self.aim[0] += 1
            self.memory_set(0x0010, 0x00)

        if self.aim == self.target:
            self.go_to_scene(Level2())


    def render(self, screen):
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 0, 0), self.aim, 5)
        pygame.draw.circle(screen, (0, 255, 0), self.target, 5)


class Level2(AsmScene):

    def __init__(self):
        super(Level2, self).__init__()
        self.bits = [
            (20,10, 50,5),
            (70,15, 5,50),
            (70,70, 5,50),
            (20,120, 50,5),
            (15,70, 5,50),
            (15,15, 5,50),
            (20,65, 50,5),
        ]
        self.off = (255, 255, 255)
        self.on = (255, 0, 0)
        self.val = 0

    def update(self, deltaTime):
        super(Level2, self).update(deltaTime)
        self.val = self.memory_fetch(0xE2)

    def render(self, screen):
        screen.fill((0, 0, 255))
        for i, b in enumerate(self.bits):
            color = self.on if self.val & int(pow(2,i)) == pow(2,i) else self.off
            pygame.draw.rect(screen, color, b)
