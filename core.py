import ctypes
import pyglet
import glooey

assets_dir = "./assets"
pyglet.resource.path.append(assets_dir)
ctypes.windll.user32.SetProcessDPIAware(2)


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


def get_triplet(*color):
    return (
        get_bgd((*color, 10)),
        get_bgd((*color, 10), (*color, 30)),
        get_bgd((*color, 30), (*color, 90)),
    )


class VariableFont:
    pass
