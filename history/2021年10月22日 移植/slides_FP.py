"""fork from FPgui v1.3"""
import os, ctypes, win32api
ctypes.windll.user32.SetProcessDPIAware(2)
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
os.environ['SDL_VIDEO_CENTERED '] = "1"
display_x, display_y = map(win32api.GetSystemMetrics, (0,1))
username = win32api.GetUserNameEx(3)

import pygame as pg; pg.init()
import numpy as np
import numba as nb
import webp
import cv2

@nb.njit(cache=True)
def dist(i, j, r):
    return ( i*i + j*j + 2*(r-i-j)*r )**0.5

@nb.njit(cache=True)
def tailor(alpha:np.ndarray, radius:float):
    w, h = alpha.shape  # pygame style
    r = int(radius) + 1
    for i in range(r):
        for j in range(r-i):
            weight = max(0.0,min(  1+radius-dist(i,j,radius)  ,1.0))
            alpha[i,j] *= weight
            alpha[-1-i,j] *= weight
            alpha[i,-1-j] *= weight
            alpha[-1-i,-1-j] *= weight

standby = 0
hovering = 1
pressing = 2
clicked = 3


class Button(pg.sprite.Sprite):
    """image based button"""
    def __init__(self, rect:pg.Rect, imgs:list[pg.Surface], callback:callable, render):
        pg.sprite.Sprite.__init__(self)
        self._situation = standby
        self.rect = rect
        self.imgs = imgs
        self.callback = callback
        self.lth = len(imgs)
        self.group:pg.sprite.RenderUpdates = render

        self.now = 0
        self.non_plateau = False

        self.image = self.imgs[0]


    @property
    def dirty(self):
        return self.dirty

    @dirty.setter
    def dirty(self, non_plateau):
        if non_plateau:
            self.non_plateau = True
            self.group.add(self)
        else:
            self.non_plateau = False
            self.group.remove(self)

    @property
    def situation(self):
        return self._situation

    @situation.setter
    def situation(self, situation):
        self._situation = situation
        self.dirty = True
        if situation == clicked:
            self.callback()
            self._situation = hovering

    def update(self):
        """frames based animation, fork from rpyg"""
        """WEB风格的按钮，只有standby<->hovering的动画"""
        if self.non_plateau:
            if self._situation in (hovering, pressing) and self.now < self.lth - 1:
                """动画正放"""
                self.now += 1
            elif self._situation == standby and self.now > 0:
                """动画倒放"""
                self.now -= 1
            else:
                """标记动画已停止"""
                self.dirty = False
                return
            """刷新"""
            self.image = self.imgs[self.now]

class UI:
    def __init__(self, screenx, screeny, flags=pg.NOFRAME, bgd=None):
        self.screen = pg.display.set_mode((screenx,screeny), flags, vsync=True)
        self.screenx, self.screeny = screenx, screeny
        self.logic = pg.sprite.Group()
        self.render = pg.sprite.RenderUpdates()
        self.clock = pg.time.Clock()
        pg.surfarray.pixels3d(self.screen)[:] = 243
        self.bgd = self.screen.copy()

    def button(self, pos, images, callback, radius=0, direction=(0,0)):
        h, w = images[0].shape[:2]
        x, y = pos

        imgs = []
        for image in images:
            imgs.append(pg.image.frombuffer(
                image, (w, h), "RGBA")
            )

        if radius:
            for img in imgs:
                tailor(pg.surfarray.pixels_alpha(img), radius)

        rect = img.get_rect()
        if direction == (0,0):
            rect.topleft = pos
        elif direction == (1,0):
            rect.topright = (self.screenx-x, y)
        elif direction == (0,1):
            rect.bottomleft = (x, self.screeny-y)
        elif direction == (1,1):
            rect.bottomright = (self.screenx-x, self.screeny-y)
        else:
            raise NotImplementedError

        self.logic.add(button:=Button(rect, imgs, callback, self.render))

        self.screen.blit(button.image, button.rect)
        pg.display.update(button.rect)

        return button

    def clear(self):
        for button in self.render:
            self.screen.blit(self.bgd, button.rect, button.rect)

    def main(self):
        hovering_button = pressed_button = None
        hovering_button:Button; pressed_button:Button

        while True:
            mouse_pos = pg.mouse.get_pos()
            for button in self.logic:
                button:Button
                if button.rect.collidepoint(mouse_pos):
                    if button is hovering_button:
                        break
                    elif hovering_button:
                        hovering_button.situation = standby
                    if button is pressed_button:
                        button.situation = pressing
                    else:
                        button.situation = hovering
                    hovering_button = button
                    break
            else:
                if hovering_button:
                    hovering_button.situation = standby
                    hovering_button = None

            for event in pg.event.get():
                if hovering_button and event.type==pg.MOUSEBUTTONDOWN and event.button==pg.BUTTON_LEFT:
                    pressed_button = hovering_button
                    pressed_button.situation = pressing
                elif pressed_button and event.type==pg.MOUSEBUTTONUP and event.button==pg.BUTTON_LEFT:
                    if pressed_button == hovering_button:
                        pressed_button.situation = clicked
                    pressed_button = None
                elif event.type == pg.QUIT:
                    return

            if hovering_button:
                pg.mouse.set_cursor(11)
            else:
                pg.mouse.set_cursor(0)
            self.logic.update()
            if self.render:
                self.clear()
                pg.display.update(self.render.draw(self.screen))
            self.clock.tick(60)

            pg.display.set_caption(f"{self.clock.get_fps()}")

if __name__ == '__main__':

    gui = UI(835, 555)
    pg.display.flip()

    title = gui.button((50,50), webp.mimread("title.webp"), lambda:None, 20)

    jump = gui.button((50,50), webp.mimread("jump.webp"), lambda:None, 20, (0,1))

    ad = gui.button((50+320+50,50), webp.mimread("ad.webp"), lambda:None, 20, (0,1))

    e = gui.button((50,50), webp.mimread("1.webp"), quit, 20, (1,0))

    n = gui.button((50,50), webp.mimread("2.webp"), lambda:None, 20, (1,1))

    gui.main()
