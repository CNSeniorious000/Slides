from core.everything import *


def alignment(widget_rect: glooey.Rect, max_rect: glooey.Rect):
    widget_rect.width = 0.7 * max_rect.width
    widget_rect.set_center(max_rect.get_center())


class Console(glooey.Form):
    custom_alignment = "fill horz"
    custom_horz_padding = after_scale(60)

    class Label(BaseLabel):
        # custom_text_alignment = "center"
        custom_font_name = "HP Simplified"
        # after_scale = lambda i:i
        custom_font_size = after_scale(24)
        custom_top_padding = custom_horz_padding = after_scale(12)
        custom_height_hint = after_scale(48)

    Base = get_bgd(preset.Vue.base_color)
    Focused = get_bgd(preset.Vue.over_color, preset.Vue.over_border_color, size=4)

    def __init__(self, text="", alignment=None):
        glooey.Form.__init__(self, text)
        self.set_alignment(alignment if alignment else self.custom_alignment)


class MainForm(UI):
    custom_size_hint = 640, 320

    def build(self):
        console = Console(alignment=alignment)
        console.push_handlers(on_unfocus=lambda w: print(f"{w.text = }"))
        self.add(console)


if __name__ == '__main__':
    with preset.Vue.using(), MainForm() as ui:
        ui.build()
