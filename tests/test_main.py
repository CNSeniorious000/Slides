from core.everything import *
import core


def test_theme():
    from core.preset import Vue
    with Vue.using():
        assert preset.used() is Vue
    assert preset.used() is preset.DefaultDark


def test_main():
    with preset.Vue.using(), UI(777, 333) as ui:
        (
            ui.add(
                VBox()
                .add(BoldButton("壹贰叁肆伍陆柒捌玖拾"))
                .add(BaseButton(core.cache_dir))
            )
        )


def test_screen_grab():
    with preset.Vue.using(), UI(640, 480) as ui:
        ui.add(button := BoldButton("截图"))

        @button.event
        def on_click(widget):
            from rich import inspect
            inspect(widget)
            pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot.png')


def test_multi_window():
    with preset.DefaultDark.using():
        UI(1920, 1080)
    with preset.DefaultLight.using():
        UI(1280, 720)
    pyglet.app.run()
