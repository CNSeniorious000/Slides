try:
    from . import *
    from . import preset
except ImportError:
    from __init__ import *
    import preset
from collections import deque
import pyglet, glooey

current_ui: "UI" = None


class UI(glooey.Gui):
    def __init__(self, *size):
        w, h = after_scale(*after_scale(*size if size else self.custom_size_hint))
        glooey.Gui.__init__(self, pyglet.window.Window(w, h, None, True))
        self.callbacks = deque()
        global current_ui
        current_ui = self

    def on_draw(self):
        for function in self.callbacks:
            function()
        glooey.Gui.on_draw(self)

    def add(self, widget):
        glooey.Gui.add(self, widget)
        return self

    def add_widget(self, widget):
        self.add(widget)
        return widget

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pyglet.app.run()


class SimplePushButton(Button):
    class Foreground(glooey.Label):
        custom_font_name = "HarmonyOS Sans SC"
        custom_font_size = after_scale(16)
        custom_color = preset.text_color
        custom_alignment = "center"

    Base, Over, Down = get_bgd_triplet(128)


class EmphasizePushButton(SimplePushButton):
    class Foreground(SimplePushButton.Foreground):
        custom_font_name = "MiSans Light"

    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self.font = preset.MiSans()
        assert isinstance(current_ui, UI)
        current_ui.callbacks.append(self.update)
        self.situation = 0

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
            self.fit()
            self.get_foreground().set_font_name(to)


class HBox(glooey.HBox):
    def add(self, widget, size=None):
        glooey.HBox.add(self, widget, size)
        return self


class VBox(glooey.VBox):
    def add(self, widget, size=None):
        glooey.HBox.add(self, widget, size)
        return self

