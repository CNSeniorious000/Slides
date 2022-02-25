import ctypes; ctypes.windll.user32.SetProcessDPIAware(2)
import pygame as pg
import pgzero.screen, pgzero.actor, pgzrun


screenx, screeny = 1280, 720

a = pgzero.actor.Actor()

def draw():
    screen = pgzero.screen.Screen(
        pg.display.set_mode((screenx, screeny), vsync=True)
    )
    screen.clear()

    screen.draw.text(
        "pygame zero test",
        centery=screeny//2, right=screenx-100,
        fontsize=32
    )

pgzrun.go()
