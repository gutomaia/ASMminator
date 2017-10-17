import wx
import pygame
### PYGAME IN WX ###
# A simple test of embedding Pygame in a wxPython frame
#
# By David Barker (aka Animatinator), 14/07/2010
# Patch for cross-platform support by Sean McKean, 16/07/2010
# Patch to fix redrawing issue by David Barker, 20/07/2010
# Second window demo added by David Barker, 21/07/2010
class PygameDisplay(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()

        self.size = self.GetSizeTuple()
        self.size_dirty = True

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.fps = 60.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)

        self.linespacing = 5

    def Update(self, event):
        self.Redraw()
        self.parent

    def Redraw(self):
        if self.size_dirty:
            self.screen = pygame.Surface(self.size, 0, 32)
            self.size_dirty = False

        self.pygame_redraw(self.timer.GetInterval())

        s = pygame.image.tostring(self.screen, 'RGB')  # Convert the surface to an RGB string
        img = wx.ImageFromData(self.size[0], self.size[1], s)  # Load this string into a wx image
        bmp = wx.BitmapFromImage(img)  # Get the image in bitmap form
        dc = wx.ClientDC(self)  # Device context for drawing the bitmap
        dc.DrawBitmap(bmp, 0, 0, False)  # Blit the bitmap image to the display
        del dc

    def pygame_redraw(self, deltaTime):
        self.screen.fill((0,0,0))
        cur = 0

        w, h = self.screen.get_size()
        while cur <= h:
            pygame.draw.aaline(self.screen, (255, 255, 255), (0, h - cur), (cur, 0))

            cur += self.linespacing

    def OnPaint(self, event):
        self.Redraw()
        event.Skip()  # Make sure the parent frame gets told to redraw as well

    def OnSize(self, event):
        self.size = self.GetSizeTuple()
        self.size_dirty = True

    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting by unbinding all methods which
        # call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        # This may or may not be necessary now that Pygame is just drawing to surfaces
        self.Unbind(event = wx.EVT_PAINT, handler = self.OnPaint)
        self.Unbind(event = wx.EVT_TIMER, handler = self.Update, source = self.timer)
