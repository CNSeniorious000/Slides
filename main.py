from core import *
from collections import deque

class BlackOnWhiteButton(glooey.Button):
    class Foreground(glooey.Label):
        custom_font_name = "MiSans Light"
        custom_font_size = 25
        custom_color = (0, 0, 0, 255)
        custom_alignment = "center"

    Base, Over, Down = get_triplet(0)

    def __init__(self, *args, **kwargs):
        glooey.Button.__init__(self, *args, **kwargs)
        w, h = self.get_foreground().do_claim()
        margin = round(h * 1.25)
        self.set_size_hint(w + margin, h + margin)

    def on_mouse_enter(self, x, y):
        glooey.Button.on_mouse_enter(self, x, y)
        self.foreground.font_name = "MiSans Normal"

    def on_mouse_leave(self, x, y):
        glooey.Button.on_mouse_leave(self, x, y)
        self.foreground.font_name = "MiSans Light"

    def on_mouse_press(self, x, y, button, modifiers):
        glooey.Button.on_mouse_press(self, x, y, button, modifiers)
        self.foreground.font_name = "MiSans Demibold"

    def on_mouse_release(self, x, y, button, modifiers):
        glooey.Button.on_mouse_release(self, x, y, button, modifiers)
        self.foreground.font_name = "MiSans Normal"

    def on_mouse_drag_leave(self, x, y):
        glooey.Button.on_mouse_drag_leave(self, x, y)
        self.foreground.font_name = "MiSans Light"


class MainForm(glooey.Gui):
    def __init__(self, w, h):
        glooey.Gui.__init__(self, pyglet.window.Window(w, h, None, True))
        self.callbacks = deque()

    def on_draw(self):
        glooey.Gui.on_draw(self)


if __name__ == '__main__':
    ui = glooey.Gui(
        window := pyglet.window.Window(480, 360, resizable=True),
        batch=(batch := pyglet.graphics.Batch()),
        group=(group := pyglet.graphics.Group()),
    )
    ui.add(get_bgd((255,))())
    ui.add(BlackOnWhiteButton("小米字体"))

    pyglet.app.run()
