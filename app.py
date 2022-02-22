from widgets import *


class MenuBar(glooey.HBox):
    def __init__(self):
        glooey.HBox.__init__(self)
        l_btn = EmphasizePushButton("左")
        r_btn = SimplePushButton("右")
        l_btn.set_alignment("left")
        r_btn.set_alignment("right")
        self.add(l_btn)
        self.add(r_btn)
        self.set_alignment("top")


class MainForm(UI):
    def __init__(self):
        UI.__init__(self, *after_scale(1280, 720))
        import widgets
        widgets.current_UI = self
        self.add(get_bgd(bg_color)())

        self.add(root_box := glooey.VBox())
        root_box.add(top_box := MenuBar())
        root_box.add(middle_grid := glooey.Grid())
        root_box.add(bottom_box := glooey.HBox())

        bottom_box.add(glooey.Placeholder(color="green"))
        bottom_box.add(glooey.Placeholder(color="white"))


if __name__ == '__main__':
    MainForm()
    pyglet.app.run()
