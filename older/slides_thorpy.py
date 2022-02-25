import ctypes; ctypes.windll.user32.SetProcessDPIAware(2)
import thorpy

app = thorpy.Application((1920,1080), "Hello world!")

btn = thorpy.make_button("Hello world!")
btn.center()

menu = thorpy.Menu(btn)
menu.play()

app.quit()
