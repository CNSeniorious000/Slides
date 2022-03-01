from contextlib import suppress
from functools import cache
from thefuzz import process
from pyperclip import copy
from rich import *
import os, sys
sys.path.append(rf"{os.path.dirname(__file__)}\..\..")
from core.everything import *

max_length = 50
n_results = 10
with suppress(ValueError):
    n_results = int(sys.argv[-1])

glossary = []
search = cache(lambda text: process.extractBests(text, glossary, limit=n_results))
# after_scale = lambda *args: args[0] if len(args) == 1 else args
for string in open("glossary.txt", "rb").read().decode().split("\r\n"):
    for i, char in enumerate(string):
        if ord(char) > ord('z'):
            left, right = string[:i], string[i:]
            print(f"[green]{left}[red]:[cyan]{right}")
            glossary.append(f"{left.strip()} {right.strip()}"[:max_length])
            break

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
        [vbox.add(Button(" " * 30, w=after_scale(800), space=0.8)) for _ in range(n_results)]
        buttons = vbox.get_children()[1:]
        callback = lambda widget: copy(widget.foreground.text)
        [button.push_handlers(on_click=callback) for button in buttons]
        last = ""

        def update():
            nonlocal last
            if last != (this := text_field.get_text()):
                last = this
                for i, result in enumerate(search(this)):
                    match, score = result
                    try:
                        button: Button = buttons[i]
                        label = button.get_foreground()
                        label.set_color((*preset.used().text_color[:3], 55 + score * 2))
                        print(f"{label.get_color() = }")
                        label.set_text(f"{match}")
                    except Exception as e:
                        print(*e.args)
                        print(f"len({match!r}) = {len(match)}")

        self.callbacks.append(update)


if __name__ == '__main__':
    with preset.Vue.using(), MainForm():
        pass
