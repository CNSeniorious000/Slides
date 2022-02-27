from contextlib import contextmanager


class Theme:  # TODO: add font_size and font_name attributes
    bgd_color = None
    base_color = over_color = down_color = None
    base_border_color = over_border_color = down_border_color = None
    text_color = None
    text_highlight_color = None
    text_highlight_bgd_color = None

    @classmethod
    def use(cls):
        global theme
        theme = cls

    @classmethod
    @contextmanager
    def using(cls):
        global theme
        last = theme
        theme = cls
        yield
        theme = last


class DefaultDark(Theme):
    bgd_color = text_highlight_color = 0, 0, 0
    base_color = over_color = 255, 255, 255, 10
    down_color = over_border_color = 255, 255, 255, 30
    down_border_color = 255, 255, 255, 90
    text_color = text_highlight_bgd_color = 255, 255, 255


class DefaultLight(Theme):
    bgd_color = text_highlight_color = 255, 255, 255
    base_color = over_color = 0, 0, 0, 10
    down_color = over_border_color = 0, 0, 0, 30
    down_border_color = 0, 0, 0, 90
    text_color = text_highlight_bgd_color = 0, 0, 0


theme = DefaultDark

def used():
    return theme


__all__ = ["DefaultDark", "DefaultLight", "used"]
