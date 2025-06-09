import textwrap
from rubicon.objc import ObjCClass
import toga

NSObject = ObjCClass("NSObject")

def wrap_text(text: str, width: int = 100) -> str:
    return textwrap.fill(text, width=width)

def set_button_enabled(app, button, value):
    invoke_later(lambda: setattr(button, 'enabled', value))

def invoke_later(fn):
    app = toga.App.app
    if app:
        app.loop.call_soon_threadsafe(fn)
    else:
        fn()
