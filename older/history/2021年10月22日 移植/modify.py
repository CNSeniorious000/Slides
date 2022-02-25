import numpy as np
import imageio
from collections import deque
import webp
import cv2
from rich import *


def animation(total:int, speed: float = 1.5):
    assert 1 < speed < total
    less = total*0.5
    sequence = deque([round(less)])
    while int(less):
        less /= speed
        sequence.appendleft(int(less))
        sequence.append(int(total-less)+1)
    print(f"{len(sequence) = }", end=" ")
    return sequence

def style_reverse(name, size=None, color=(179,55,55)):
    a = np.median(imageio.imread(f"{name}.png"), axis=2)  # take luma as alpha
    if size:
        a = cv2.resize(a, size, interpolation=cv2.INTER_AREA)
    h, w = a.shape
    b = 255 - a

    s = animation(255)

    out = [np.tile(np.array([*color, 0], np.uint8), w*h).reshape((h,w,4)) for i in s]
    for i, j in enumerate(s):
        j /= 255
        out[i][..., 3] = a * j + b * (1 - j)

    webp.mimwrite(f"{name}.webp", out, lossless=1, fps=60)
    print(f"[u] style reverse [/u] {name} completed")

def style_layer(name, size=None, color=(55,179,179)):
    a = np.median(imageio.imread(f"{name}.png"), axis=2)  # take luma as alpha
    if size:
        a = cv2.resize(a, size, interpolation=cv2.INTER_AREA)
    h, w = a.shape
    b = 255 - a

    s = animation(255)

    out = [np.tile(np.array([*color, 0], np.uint8), w*h).reshape((h,w,4)) for i in s]
    for i, j in enumerate(s):
        j /= 255
        out[i][..., 3] = b + 0.25 * a * j
    webp.mimwrite(f"{name}.webp", out, lossless=1, fps=60)
    print(f"[u] style layer [/u] {name} completed")

def style_fill(name, size=None, color=(55,179,55)):
    a = np.median(imageio.imread(f"{name}.png"), axis=2)  # take luma as alpha
    if size:
        a = cv2.resize(a, size, interpolation=cv2.INTER_AREA)
    h, w = a.shape
    b = 255-a

    s = animation(w)

    out = [np.tile(np.array([*color, 0], np.uint8), w*h).reshape((h,w,4)) for i in s]
    for i, j in enumerate(s):
        out[i][..., 3] = b
        out[i][:, :j, 3] = a[:, :j]
    webp.mimwrite(f"{name}.webp", out, lossless=1, fps=60)
    print(f"[u] style fill [/u] {name} completed")

"""TODO: 把读图、取图、获取sequence的操作抽象成单独函数，传入用numba实现的backend"""

def blend_fill(name, size=None):
    a = imageio.imread(f"{name}1.png")
    b = imageio.imread(f"{name}2.png")
    if size:
        a = cv2.resize(a, size, interpolation=cv2.INTER_AREA)
        b = cv2.resize(b, size, interpolation=cv2.INTER_AREA)
    h, w, c = a.shape

    s = animation(w)

    out = [np.zeros([h, w, c], np.uint8) for i in s]
    for i, j in enumerate(s):
        out[i][:] = a
        out[i][:, :j] = b[:, :j]
    webp.mimwrite(f"{name}.webp", out, lossless=1, fps=60)
    print(f"[u] blend fill [/u] {name} completed")

def blend_alpha(name, size=None, n=8):
    a = imageio.imread(f"{name}1.png")
    b = imageio.imread(f"{name}2.png")
    if size:
        a = cv2.resize(a, size, interpolation=cv2.INTER_AREA)
        b = cv2.resize(b, size, interpolation=cv2.INTER_AREA)
    h, w, c = a.shape

    s = animation(255)

    out = [np.zeros([h, w, c], np.uint8) for i in s]
    for i, j in enumerate(s):
        j /= 255
        out[i][:] = b * j + a * (1 - j)
    webp.mimwrite(f"{name}.webp", out, lossless=1, fps=60)
    print(f"[u] blend alpha [/u] {name} completed")


if __name__ == '__main__':

    style_reverse("1", (45,45))
    style_layer("2", (45,45))

    blend_fill("jump", (320,45))
    blend_alpha("title", (640, 360))
    blend_alpha("ad", (270,45))
