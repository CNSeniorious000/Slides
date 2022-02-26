from core.everything import *


class MenuBar(HBox):
    def __init__(self):
        glooey.HBox.__init__(self)
        l_btn = EmphasizePushButton("←")
        r_btn = SimplePushButton("右右右右右右右右右右")
        l_btn.set_alignment("left")
        r_btn.set_alignment("right")
        self.add(l_btn)
        self.add(r_btn)
        self.set_alignment("top")


class MainForm(UI):
    custom_size_hint = 1280, 720

    def build(self):
        (
            self.add(get_bgd(preset.bg_color)())
                .add_widget(VBox())
                .add(top_box := MenuBar())
                .add(middle_grid := glooey.Grid())
                .add(bottom_box := HBox())
        )

        bottom_box.add(glooey.Placeholder(color="green"))
        bottom_box.add(glooey.Placeholder(color="white"))


if __name__ == '__main__':
    with MainForm() as ui:
        ui.build()
