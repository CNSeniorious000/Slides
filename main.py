from core import *
import preset
from collections import deque


class MaterialButton(Button):
    class Foreground(glooey.Label):
        custom_font_name = "MiSans Light"
        custom_font_size = 13
        custom_color = (0, 0, 0, 255)
        custom_alignment = "center"

    Base, Over, Down = get_bgd_triplet(128)


class SimpleButton(Button):
    class Foreground(glooey.Label):
        custom_font_name = "MiSans Light"
        custom_font_size = 20
        custom_color = (0, 0, 0, 255)
        custom_alignment = "center"

    Base, Over, Down = get_bgd_triplet(128, bordered=False)

    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self.font = preset.MiSans()
        self.situation = 0
        self.get_foreground().set_style()

    def on_mouse_enter(self, x, y):
        Button.on_mouse_enter(self, x, y)
        self.situation = 1

    def on_mouse_leave(self, x, y):
        Button.on_mouse_leave(self, x, y)
        self.situation = -1

    def on_mouse_drag_leave(self, x, y):
        Button.on_mouse_drag_leave(self, x, y)
        self.situation = -1

    @property
    def next_font(self):
        return self.font.heavier if ~ self.situation else self.font.thinner

    def update(self):
        if self.situation and (to := self.next_font):
            print(f"{to = }")
            self.get_foreground().set_font_name(to)


class MainForm(glooey.Gui):
    def __init__(self, w, h):
        glooey.Gui.__init__(self, pyglet.window.Window(w, h, None, True))
        self.callbacks = deque()

    def on_draw(self):
        for widget in self.get_children():
            try:
                widget.update()
            except AttributeError:
                pass
        glooey.Gui.on_draw(self)


if __name__ == '__main__':
    ui = MainForm(720, 480)
    ui.add(get_bgd((255,))())
    ui.add(box := glooey.VBox())
    box.add(SimpleButton("一二三四五六七八九十"))  # 这里出问题了，button不是gui的直系children
    box.add(MaterialButton("一二三四五六七八九十"))

    pyglet.app.run()
