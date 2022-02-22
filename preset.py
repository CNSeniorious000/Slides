from core import *

class MiSans(VariableFont):
    def __init__(self):
        VariableFont.__init__(
            self,
            """
MiSans Thin
MiSans ExtraLight
MiSans Light
MiSans Normal
MiSans
MiSans Medium
MiSans Demibold
MiSans Semibold
MiSans Bold
MiSans Heavy
            """.strip().split('\n'),
            2, 7
        )

class HarmonyOSSans(VariableFont):
    def __init__(self):
        VariableFont.__init__(
            self,
            """
HarmonyOS Sans SC Thin
HarmonyOS Sans SC Light
HarmonyOS Sans SC
HarmonyOS Sans SC Medium
HarmonyOS Sans SC Bold
HarmonyOS Sans SC Black
            """.strip().split('\n'),
            0, 3
        )
