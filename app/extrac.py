from kivy.app import App
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
        """Set default settings for the application
            Currency   : currency symbol to be used
            Mode       : Whether Dark or Light mode
            DayLimitFlg: Enable or disable app theme color change on breach of
                         daily spend limit.
            DayLimitAmt: Daily spend limit
        """
        config.setdefaults('CustSettings', {'Currency': '₹',
                                            'Mode': 'Light',
                                            'DayLimitFlg': False,
                                            'DayLimitAmt': 0})

    def on_start(self):
        """On Application start show the startup screen"""
        ss = StartupScreen()
        self.root.add_widget(ss)
        self.root.current = 'StartupScreen'


