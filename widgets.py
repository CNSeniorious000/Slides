from collections import deque
from core import *
import preset

current_UI: "UI" = None

bg_color = (0, 0, 0)
fg_color = (128, 128, 128, 255)
text_color = (255, 255, 255, 255)


class SimplePushButton(Button):
    Base, Over, Down = get_bgd_triplet(128)

    class Foreground(glooey.Label):
        custom_font_name = "HarmonyOS Sans SC Light"
        custom_font_size = after_scale(16)
        custom_color = text_color
        custom_alignment = "center"


class EmphasizePushButton(Button):
    Base, Over, Down = get_bgd_triplet(128)

    class Foreground(glooey.Label):
        custom_font_name = "MiSans Light"
        custom_font_size = after_scale(16)
        custom_color = text_color
        custom_alignment = "center"

    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self.font = preset.MiSans()
        self.situation = 0
        assert isinstance(current_UI, UI)
        current_UI.callbacks.append(self.update)

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
            # print(f"{to = }")
            self.get_foreground().set_font_name(to)


class UI(glooey.Gui):
    def __init__(self, w, h):
        glooey.Gui.__init__(self, pyglet.window.Window(w, h, None, True))
        self.callbacks = deque()

    def on_draw(self):
        for function in self.callbacks:
            function()
        glooey.Gui.on_draw(self)


def setup(w, h):
    global current_UI
    current_UI = UI(*after_scale(w, h))


if __name__ == '__main__':
    setup(1920, 1080)
    current_UI.add(get_bgd(bg_color)())
    current_UI.add(box := glooey.VBox())

    box.add(s := EmphasizePushButton("适用大字号の按钮"))
    box.add(SimplePushButton("适用稍小字号の按钮"))

    pyglet.app.run()
