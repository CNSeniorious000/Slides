import ctypes
import pyglet
import glooey

__all__ = [
    "after_scale",
    "get_block",
    "get_bgd",
    "get_bgd_triplet",
    "VariableFont",
    "Button",
]
try:
    pyglet.resource.path.append(cache_dir := rf"{__path__[0]}\cache")
except NameError:
    pyglet.resource.path.append(cache_dir := "cache")  # in case debug from within package
ctypes.windll.user32.SetProcessDPIAware(2)
factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)


def after_scale(*numbers):
    if len(numbers) == 1:
        return int(numbers[0] * factor // 100)
    else:
        return [int(number * factor // 100) for number in numbers]


def get_block(size, *color):
    file_name = f"{size}_{'_'.join(map(str, color))}.png"
    try:
        return pyglet.resource.texture(file_name)
    except pyglet.resource.ResourceNotFoundException:
        import numpy as np, cv2
        match color:
            case (k, ): arr = np.full((size, size), k)
            case (l, a): arr = np.full((size, size, 4), (l, l, l, a))
            case (r, g, b): arr = np.full((size, size, 3), (b, g, r))
            case (r, g, b, a): arr = np.full((size, size, 4), (b, g, r, a))
            case _: raise TypeError(*color)
        print(f"{cache_dir}\\{file_name}")
        cv2.imwrite(f"{cache_dir}\\{file_name}", arr)
        pyglet.resource.reindex()
        return pyglet.resource.texture(file_name)


def get_bgd(inner, outer=None, *, size=2):
    # TODO: to support non-2-power border value
    class _(glooey.Background):
        custom_center = get_block(size, *inner)
        if outer is not None:
            block_outer = get_block(size, *outer)
            custom_top = block_outer
            custom_bottom = block_outer
            custom_left = block_outer
            custom_right = block_outer
            custom_top_left = block_outer
            custom_top_right = block_outer
            custom_bottom_left = block_outer
            custom_bottom_right = block_outer

    return _


def get_bgd_triplet(*color, bordered=True):
    return (
        get_bgd((*color, 20)[:3]),
        get_bgd((*color, 20)[:3], (*color, 60)[:3] if bordered else None),
        get_bgd((*color, 60)[:3], (*color, 180)[:3] if bordered else None),
    )


class VariableFont:
    def __init__(self, paths, min_, max_):
        self.paths = paths
        self.min = min_
        self.max = max_
        self.now = min_

    @property
    def heavier(self) -> str | None:
        if self.now < self.max:
            self.now += 1
            return self.paths[self.now]

    @property
    def thinner(self) -> str | None:
        if self.now > self.min:
            self.now -= 1
            return self.paths[self.now]


class Button(glooey.Button):
    def __init__(self, *args, w=None, h=None, space=1.25, **kwargs):
        glooey.Button.__init__(self, *args, **kwargs)
        self.w = w
        self.h = h
        self.space = space
        self.set_size_hint(w, h) if w and h else self.fit()

    def fit(self):
        w, h = self.w, self.h
        if w and h:
            return print("skipped")
        w_hint, h_hint = self.get_foreground().do_claim()
        margin = round(h_hint * self.space)
        return self.set_size_hint(w or w_hint + margin, h or h_hint + margin)
