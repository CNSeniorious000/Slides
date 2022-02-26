try:
    from . import VariableFont
except ImportError:
    from __init__ import VariableFont


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
            ], 2, 7
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


bg_color = (0, 0, 0)
fg_color = (128, 128, 128)
text_color = (255, 255, 255)
