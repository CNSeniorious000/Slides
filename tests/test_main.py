from core.everything import *
import core

def test_path():
    with UI(444, 222) as ui:
        (
            ui.add(get_bgd(preset.bg_color)())
            .add_widget(VBox())
            .add(EmphasizePushButton("适用大字号の按钮"))
            .add(SimplePushButton(core.cache_dir))
        )
