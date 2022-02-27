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
        w, h = after_scale(*size if size else self.custom_size_hint)
        glooey.Gui.__init__(self, pyglet.window.Window(w, h, None, True))
        self.callbacks = deque()
        global current_ui
        current_ui = self
        self.add_back(get_bgd(preset.used().bgd_color)())

    def on_draw(self):
        for function in self.callbacks:
            function()
        glooey.Gui.on_draw(self)

    def add(self, widget):
        glooey.Gui.add(self, widget)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pyglet.app.run()


class HBox(glooey.HBox):
    def add(self, widget, size=None):
        glooey.HBox.add(self, widget, size)
        return self


class VBox(glooey.VBox):
    def add(self, widget, size=None):
        glooey.HBox.add(self, widget, size)
        return self


class BaseButton(Button):
    class Foreground(glooey.Label):
        custom_font_name = "HarmonyOS Sans SC"
        custom_font_size = after_scale(16)
        custom_alignment = "center"

    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self.theme = preset.used()
        self.stylize()

    def stylize(self):
        theme = self.theme
        self.get_foreground().set_color(theme.text_color)
        self.set_base_background(get_bgd(theme.base_color, theme.base_border_color)())
        self.set_over_background(get_bgd(theme.over_color, theme.over_border_color)())
        self.set_down_background(get_bgd(theme.down_color, theme.down_border_color)())


class AniButton(BaseButton):
    def __init__(self, *args, **kwargs):
        BaseButton.__init__(self, *args, **kwargs)
        current_ui.callbacks.append(self.update)
        self.situation = 0

        @self.event("on_mouse_hold")
        @self.event("on_mouse_enter")
        @self.event("on_mouse_motion")
        def on_enter(*_):
            self.situation = 1

        @self.event("on_mouse_leave")
        @self.event("on_mouse_drag_leave")
        def on_leave(*_):
            self.situation = -1

    def update(self):
        return NotImplemented


class BoldButton(AniButton):
    class Foreground(BaseButton.Foreground):
        custom_font_name = "MiSans Light"

    def __init__(self, *args, **kwargs):
        self.font = preset.MiSans()
        AniButton.__init__(self, *args, **kwargs)
        current_ui.callbacks.append(self.update)
        self.situation = 0

    @property
    def next_font(self):
        return self.font.heavier if ~ self.situation else self.font.thinner

    def update(self):
        if self.situation and (to := self.next_font):
            self.get_foreground().set_font_name(to)
            self.fit()


class BaseLabel(glooey.EditableLabel):
    custom_kerning = 0.5

    def __init__(self, text="", line_wrap=None):
        glooey.EditableLabel.__init__(self, text, line_wrap)
        self.theme = preset.used()
        self.stylize()

    def stylize(self):
        theme = self.theme
        self.set_color(theme.text_color)
        self.set_selection_color(theme.text_highlight_color)
        self.set_selection_background_color(theme.text_highlight_bgd_color)
