import sys

sys.path.append("..")
from core.everything import *


class Completion(glooey.Form):
    class Label(BaseLabel):
        custom_text_alignment = "center"
        custom_font_name = "HP Simplified"
        custom_font_size = after_scale(32)
        custom_top_padding = custom_horz_padding = after_scale(16)
        custom_height_hint = after_scale(64)

    Base = get_bgd(preset.Vue.base_color)
    Focused = get_bgd(preset.Vue.over_color, preset.Vue.over_border_color, size=4)
    custom_alignment = "center"


preset.Vue.use()
ui = UI(400, 180)
last = ""


def resize():
    global last
    label = textbox.get_label()
    if last != (this := label.get_text()):
        last = this
        width = len(this) * label.font_size * 0.75
        print(width)
        label.set_width_hint(width)


textbox = Completion("type here")
ui.callbacks.append(resize)
ui.add(textbox)
pyglet.app.run()
