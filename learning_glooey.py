from core import *

# style = pyglet.window.Window.WINDOW_STYLE_TRANSPARENT
style = None

ui = glooey.Gui(
    window := pyglet.window.Window(480, 360, resizable=True, style=style),
    batch=(batch := pyglet.graphics.Batch()),
    group=(group := pyglet.graphics.Group()),
)

ui.add(get_bgd((255,))())


class BlackOnWhiteButton(glooey.Button):
    class Foreground(glooey.Label):
        custom_font_name = "JetBrains Mono"
        custom_font_size = 10
        custom_color = (0, 0, 0, 255)
        custom_alignment = "center"

    Base, Over, Down = get_bgd_triplet(128)

    def on_mouse_enter(self, x, y):
        super().on_mouse_enter(x, y)

    def __init__(self, *args, **kwargs):
        glooey.Button.__init__(self, *args, **kwargs)
        self.set_size_hint(100, 50)
        w, h = self.get_foreground().do_claim()
        self.set_size_hint(w + h * 2, h * 3)

    def on_mouse_motion(self, x, y, dx, dy):
        print(self.get_foreground().get_claimed_size())


ui.add(BlackOnWhiteButton("click me"))

if __name__ == '__main__':
    pyglet.app.run()
