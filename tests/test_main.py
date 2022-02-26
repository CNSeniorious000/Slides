from core.everything import *
import core


def test_path():
    with UI(777, 333) as ui:
        (
            ui.add(get_bgd(preset.bg_color)())
            .add(
                VBox()
                .add(EmphasizePushButton("12345678901234567890"))
                .add(SimplePushButton(core.cache_dir))
            )
        )
