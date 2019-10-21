# Entry point to the application. Runs the main extrac.py program code.
# In case of error, displays a window with its text.

import os
import sys
import traceback

directory = os.path.dirname(__file__)

try:

    from kivy.config import Config
    Config.set('kivy', 'keyboard_mode', 'system')
    Config.set('kivy', 'log_enable', 0)

except Exception:
    traceback.print_exc(file=open(os.path.join(directory, 'error.log'), 'w'))
    print(traceback.print_exc())
    sys.exit(1)


def main():

    try:
        from extrac import EXTrac

        app = EXTrac()
        app.run()
    except Exception:
        from kivy.app import App
        from kivy.uix.boxlayout import BoxLayout

        def create_error_monitor():
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.label import Label
            from kivy.uix.textinput import TextInput

            class _App(App):
                def build(self):
                    box = BoxLayout()
                    box.add_widget(TextInput(text=text_error, size_hint_x=0.9, multiline=True))
                    return box
            app2 = _App()
            try:
                app2.run()
            except Exception as e:
                pass

        text_error = traceback.format_exc()

        with open(os.path.join(directory, 'error.log'), 'w') as fd:
            traceback.print_exc(file=fd)

        create_error_monitor()


if __name__ in ('__main__', '__android__'):
    main()
