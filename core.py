import ctypes
import pyglet
import glooey

assets_dir = "./assets"
pyglet.resource.path.append(assets_dir)
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
            case (k, ):
                arr = np.full((size, size), k)
            case (l, a):
                arr = np.full((size, size, 4), (l, l, l, a))
            case (r, g, b):
                arr = np.full((size, size, 3), (r, g, b))
            case (r, g, b, a):
                arr = np.full((size, size, 4), (r, g, b, a))
            case _:
                raise TypeError(*color)
        cv2.imwrite(f"{assets_dir}/{file_name}", arr)
        pyglet.resource.reindex()
        return pyglet.resource.texture(file_name)


def get_bgd(inner, outer=None, *, size=2):
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
        get_bgd((*color, 20)),
        get_bgd((*color, 20), (*color, 60) if bordered else None),
        get_bgd((*color, 60), (*color, 180) if bordered else None),
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
    def __init__(self, *args, **kwargs):
        glooey.Button.__init__(self, *args, **kwargs)
        self.fit()

    def fit(self):
        w, h = self.get_foreground().do_claim()
        margin = round(h * 1.25)
        self.set_size_hint(w + margin, h + margin)
