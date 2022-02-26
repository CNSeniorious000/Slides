from core.everything import (
    EmphasizePushButton, SimplePushButton, UI,
    glooey, after_scale, get_bgd, preset, get_bgd_triplet
)


def alignment(widget_rect: glooey.Rect, max_rect: glooey.Rect):
    widget_rect.width = 0.7 * max_rect.width
    widget_rect.set_center(max_rect.get_center())


class Console(glooey.Form):
    custom_alignment = "fill horz"
    custom_horz_padding = after_scale(60)

    class Label(glooey.EditableLabel):
        custom_text_alignment = "center"
        custom_font_name = "Unifont CSUR"
        custom_font_size = after_scale(40)
        custom_top_padding = custom_horz_padding = after_scale(32)
        custom_height_hint = after_scale(96)
        custom_color = preset.text_color

    Base = get_bgd((128, 20))
    Focused = get_bgd((128, 30), (128, 150), size=1)

    def __init__(self, text="", alignment=None):
        glooey.Form.__init__(self, text)

        # w_hint, h_hint = self.get_label().do_claim()
        # margin = h_hint * 4
        # self.set_size_hint(w_hint + margin, h_hint + margin)

        self.set_alignment(alignment if alignment else self.custom_alignment)


class MainForm(UI):
    custom_size_hint = 640, 320

    def build(self):
        self.add(get_bgd(preset.bg_color)())

        console = Console(alignment=alignment)
        console.push_handlers(on_unfocus=lambda w: print(f"{w.text = }"))
        self.add(console)


if __name__ == '__main__':
    with MainForm() as ui:
        ui.build()
