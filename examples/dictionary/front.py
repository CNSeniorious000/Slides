import os, sys

sys.path.append(rf"{os.path.dirname(__file__)}\..\..")
from core.everything import *


# after_scale = lambda i:i

def alignment(widget_rect: glooey.Rect, max_rect: glooey.Rect):
    widget_rect.set_width(max_rect.get_width() * 0.8)
    widget_rect.set_center(max_rect.get_center())


class Console(glooey.Form):
    custom_alignment = "fill horz"
    custom_horz_padding = after_scale(60)

    class Label(BaseLabel):
        # custom_text_alignment = "center"
        custom_font_name = "Fira Code"
        custom_font_size = after_scale(24)
        custom_top_padding = custom_horz_padding = after_scale(12)
        custom_height_hint = after_scale(48)

    Base = get_bgd(preset.Vue.base_color)
    Focused = get_bgd(preset.Vue.over_color, preset.Vue.over_border_color)


class Button(BoldButton):
    custom_alignment = "fill"

    class Foreground(BoldButton.Foreground):
        custom_left_padding = after_scale(16)
        custom_alignment = "left"


class MainForm(UI):
    custom_size_hint = 600, 1000

    def build(self):
        vbox = VBox()
        vbox.set_padding(after_scale(12))
        vbox.set_alignment(alignment)
        console = Console()
        console.push_handlers(on_unfocus=lambda w: print(f"{w.text = }"))
        vbox.add(console)
        self.add(vbox)

        for i in range(10):
            vbox.add(Button("12312334234"[i] * 10, auto=True))

    def on_resize(self, width, height):
        UI.on_resize(self, width, height)


if __name__ == '__main__':
    with preset.Vue.using(), MainForm() as ui:
        ui.build()
