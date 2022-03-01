try:
    from . import VariableFont
    from .theme import *
except ImportError as ex:
    print(ex)
    from __init__ import VariableFont
    from theme import *


class MiSans(VariableFont):
    def __init__(self):
        VariableFont.__init__(
            self, [
                "MiSans Thin",
                "MiSans ExtraLight",
                "MiSans Light",
                "MiSans Normal",
                "MiSans",
                "MiSans Medium",
                "MiSans Demibold",
                "MiSans Semibold",
                "MiSans Bold",
                "MiSans Heavy",
            ], 3, 7
        )


class HarmonyOSSans(VariableFont):
    def __init__(self):
        VariableFont.__init__(
            self, [
                "HarmonyOS Sans SC Thin",
                "HarmonyOS Sans SC Light",
                "HarmonyOS Sans SC",
                "HarmonyOS Sans SC Medium",
                "HarmonyOS Sans SC Bold",
                "HarmonyOS Sans SC Black",
            ], 0, 3
        )


class Vue(DefaultLight):
    text_color = 53, 73, 94
    down_color = 53, 73, 94, 20
    bgd_color = 246, 246, 246
    base_color = over_color = text_highlight_color = 255, 255, 255, 255
    over_border_color = down_border_color = text_highlight_bgd_color = 66, 185, 131, 255
