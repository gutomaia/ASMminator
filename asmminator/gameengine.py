from ui import PygameDisplay
import pygame


class SceneBase(object):

    def __init__(self):
        self.next = self
        self.context = {}

    def input_code(self, source):
        try:
            compiled = compile(source, '<string>', 'exec') # gives syntax error
            exec(compiled, self.context) # gives generic exceptions
        except SyntaxError, e:
            print 'syntax error', e
        except Exception, e:
            print 'exception', e

    def update(self, deltaTime):
        pass

    def render(self, screen):
        pass

    def go_to_scene(self, next_scene):
        self.next = next_scene

    def terminate(self):
        self.go_to_scene(None)


class DisplayScene(PygameDisplay):

    def __init__(self, parent, ID, starting_scene=None):
        super(DisplayScene, self).__init__(parent, ID)
        import sys
        # pygame.init()


        if not starting_scene:
            self.active_scene = TitleScene()
        else:
            self.active_scene = starting_scene

    def pygame_redraw(self, deltaTime):
        self.active_scene.update(deltaTime)
        self.active_scene.render(self.screen)
        self.active_scene = self.active_scene.next

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                self.go_to_scene(GameScene())

    def update(self, deltaTime):
        pass

    def render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((255, 0, 0))

class GameScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def process_input(self, events, pressed_keys):
        pass

    def update(self, deltaTime):
        pass

    def render(self, screen):
        # The game scene is just a blank blue screen
        screen.fill((0, 0, 255))
