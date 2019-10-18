from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, DictProperty
from kivy.uix.screenmanager import ScreenManager

from startupscreen import startupscreen, StartupScreen


class EXTrac(App):
    title = 'Expense Tracker'
    date = None
    screens = ObjectProperty()
    item_selection = DictProperty()

    def __init__(self, **kwargs):
        super(EXTrac, self).__init__(**kwargs)

    def build(self):
        self.use_kivy_settings = False
        sm = ScreenManager()
        return sm

    def build_config(self, config):
        config.setdefaults('CustSettings', {'Currency': '₹',
                                            'Mode': 'Light',
                                            'DayLimitFlg': False,
                                            'DayLimitAmt': 0})

    def on_start(self):
        Builder.load_string(startupscreen)
        ss = StartupScreen()
        self.root.add_widget(ss)
        self.root.current = 'StartupScreen'


