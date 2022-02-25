import ctypes; ctypes.windll.user32.SetProcessDPIAware(2)
import pygame as pg
import pygame_gui as gui

pg.init()

pg.display.set_caption('Quick Start')
screen = pg.display.set_mode((800, 600))

background = pg.Surface((800, 600))
background.fill(pg.Color('#000000'))

ui = gui.UIManager((800, 600))
ui.set_visual_debug_mode(True)
btn_hello = gui.elements.UIButton(
    pg.Rect(350,275,100,50), "say hello", ui
)

clock = pg.time.Clock()

is_running = True

while is_running:
    dt = clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False
        elif event.type == pg.USEREVENT:
            if event.user_type == gui.UI_BUTTON_PRESSED:
                if event.ui_element == btn_hello:
                    print("hello world")

        ui.process_events(event)

    ui.update(dt / 1000)

    screen.blit(background, (0, 0))
    ui.draw_ui(screen)

    pg.display.update()
