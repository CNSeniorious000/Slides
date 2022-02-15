import ctypes
import pyglet
import glooey

ctypes.windll.user32.SetProcessDPIAware(2)
pyglet.resource.path.append("./assets")
style = pyglet.window.Window.WINDOW_STYLE_TRANSPARENT

ui = glooey.Gui(
    window := pyglet.window.Window(480, 360, resizable=True, style=style),
    batch=(batch := pyglet.graphics.Batch()),
    group=(group := pyglet.graphics.Group())
)


class Border(glooey.Background):
    custom_center = pyglet.resource.texture('center.png')
    custom_top = pyglet.resource.texture('top.png')
    custom_bottom = pyglet.resource.texture('bottom.png')
    custom_left = pyglet.resource.texture('left.png')
    custom_right = pyglet.resource.texture('right.png')
    custom_top_left = pyglet.resource.image('top_left.png')
    custom_top_right = pyglet.resource.image('top_right.png')
    custom_bottom_left = pyglet.resource.image('bottom_left.png')
    custom_bottom_right = pyglet.resource.image('bottom_right.png')


ui.add_back(Border())


class Button(glooey.Button):
    class Foreground(glooey.Label):
        custom_font_name = "JetBrains Mono"
        custom_font_size = 10
        custom_color = (255, 155, 55, 255)
        custom_alignment = "center"

    # class Base(glooey.Image):
    #     custom_image = pyglet.resource.image("base.png")

    class Over(glooey.Image):
        custom_image = pyglet.resource.image("over.png")

    class Down(glooey.Image):
        custom_image = pyglet.resource.image("down.png")


ui.add(Button("click me"))

if __name__ == '__main__':
    pyglet.app.run()
