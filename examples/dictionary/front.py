import os, sys; sys.path.append(rf"{os.path.dirname(__file__)}\..\..")
from core.everything import *
from pyperclip import copy
from contextlib import suppress
from thefuzz import process
from functools import cache

n_results = 10
with suppress(ValueError):
    n_results = int(sys.argv[-1])

glossary = open("glossary.txt", "rb").read().decode().split("\r\n")
search = cache(lambda text: process.extractBests(text, glossary, limit=n_results))
# after_scale = lambda _:_


class Console(glooey.Form):
    custom_alignment = "fill horz"

    class Label(BaseLabel):
        # custom_text_alignment = "center"
        custom_font_name = "HP Simplified"
        custom_font_size = after_scale(16)
        custom_top_padding =custom_horz_padding = after_scale(8)
        custom_height_hint = after_scale(32)

    Base = get_bgd(preset.Vue.base_color)
    Focused = get_bgd(preset.Vue.over_color, preset.Vue.over_border_color)


class Button(BoldButton):
    custom_alignment = "fill horz"

    class Foreground(BoldButton.Foreground):
        custom_left_padding = after_scale(8)
        custom_font_size = after_scale(16)
        custom_alignment = "left"


class MainForm(UI):
    custom_size_hint = 80, 1000

    def __init__(self, *size):
        UI.__init__(self, *size)
        vbox = VBox().add(console := Console())
        vbox.padding = after_scale(12)
        vbox.aliment = "fill horz"
        [vbox.add(Button(" ", after_scale(300), auto=True, space=0.5)) for _ in range(n_results)]
        buttons = vbox.get_children()[1:]
        callback = lambda widget: copy(widget.foreground.text)
        [button.push_handlers(on_click=callback) for button in buttons]
        last = " "

        def update():
            nonlocal last
            if last != (this := console.get_text()):
                last = this

        try:
            self.add(vbox)
        except RuntimeError as ex:
            with suppress(ValueError):
                key = "but its children are "
                message = ex.args[0]
                print(message)
                left = message.index(key) + len(key)
                w, h = message[left:-1].split("x")
                print(f"{w = }, {h = }")
                exit(1)


if __name__ == '__main__':
    with preset.Vue.using(), MainForm():
        pass