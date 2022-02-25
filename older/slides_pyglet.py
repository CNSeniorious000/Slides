import ctypes; ctypes.windll.user32.SetProcessDPIAware(2)
from rich import *
import pyglet


pyglet.resource.path.append("../RPG")
pyglet.resource.path.append("../RPG/cache")
pyglet.resource.reindex()

img = pyglet.resource.image("Why_PM_2_3.cachr.png")
inspect(img)

img:pyglet.image.Texture
img:pyglet.image.TextureRegion

window = pyglet.window.Window(width=img.width, height=img.height)

@window.event
def on_draw():
    window.clear()
    img.blit(0,0)

pyglet.app.run()
