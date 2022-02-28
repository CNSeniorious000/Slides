from contextlib import suppress
from threading import Thread
from functools import cache
from thefuzz import process
from pyperclip import copy
from time import sleep
import os, sys
sys.path.append(rf"{os.path.dirname(__file__)}\..\..")
from core.everything import *

n_results = 10
with suppress(ValueError):
    n_results = int(sys.argv[-1])

glossary = open("glossary.txt", "rb").read().decode().split("\r\n")
search = cache(lambda text: process.extractBests(text, glossary, limit=n_results))
after_scale = lambda *args: args[0] if len(args) == 1 else args


class VueForm(glooey.Form):
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
    custom_size_hint = after_scale(600, 48 * n_results)

    def __init__(self):
        UI.__init__(self)
        vbox = VBox().add(text_field := VueForm())
        self.add(vbox)
        vbox.padding = after_scale(12)
        vbox.aliment = "fill horz"
        [vbox.add(Button(" "*30, space=0.5)) for _ in range(n_results)]
        buttons = vbox.get_children()[1:]
        callback = lambda widget: copy(widget.foreground.text)
        [button.push_handlers(on_click=callback) for button in buttons]
        last = ""

        def update():
            nonlocal last
            if last != (this := text_field.get_text()):
                last = this
                print(this)
                for i, result in enumerate(search(this)):
                    match, score = result
                    try:
                        buttons[i].get_foreground().set_text(f"{match} @ {score}")
                    except Exception as e:
                        print(e.args)
            sleep(1/30)

        self.callbacks.append(update)

        #
        # try:
        #     self.add(vbox)
        # except RuntimeError as ex:
        #     with suppress(ValueError):
        #         key = "but its children are "
        #         message = ex.args[0]
        #         print(message)
        #         left = message.index(key) + len(key)
        #         w, h = message[left:-1].split("x")
        #         print(f"{w = }, {h = }")
        #         exit(1)


if __name__ == '__main__':
    with preset.Vue.using(), MainForm():
        pass
