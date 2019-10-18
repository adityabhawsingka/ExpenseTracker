from kivy.uix.screenmanager import Screen
from kivymd.label import MDLabel
from kivy.uix.dropdown import DropDown
from kivy.uix.behaviors import ButtonBehavior


settings_kv = '''
#:import MDTextField kivymd.textfields.MDTextField
#:import MDSwitch kivymd.selectioncontrols.MDSwitch
#:import MDLabel kivymd.label.MDLabel

<SettingsPage>:
    currency: currency
    ScrollView:
        FloatLayout:
            FloatLayout:
                size_hint_y: None
                height : currency.size[1]
                pos_hint: {'x': 0, 'y': .85}
                canvas.before:
                    Color:
                        rgba: app.theme_cls.divider_color
                    Line:
                        width: .5
                        points: [self.x + 5, self.y, self.x - 5 + self.width, self.y ]
                MDLabel:
                    size_hint_x: .4
                    pos_hint: {'x': .05, 'y': .1}
                    text: 'Currency'
                    halign: 'left'
                    theme_text_color: "Primary"
                MDRectangleFlatButton:
                    id: currency
                    size_hint_x: .4
                    pos_hint: {'x': .5, 'y': .1}                    
                    theme_text_color: "Primary"
            FloatLayout:
                size_hint_y: None
                height : currency.size[1]
                pos_hint: {'x': 0, 'y': .73}
                canvas.before:
                    Color:
                        rgba: app.theme_cls.divider_color
                    Line:
                        width: .5
                        points: [self.x + 5, self.y, self.x - 5 + self.width, self.y ]                
                MDLabel:
                    size_hint_x: .4
                    pos_hint: {'x': .05, 'y': .05}                
                    text: 'Dark Mode'
                    halign: 'left'
                    theme_text_color: "Primary"
                MDSwitch:
                    id: darkmode
                    size_hint_x: .1
                    pos_hint: {'x': .52, 'y': .05}  
                    on_active: root.dark_mode()
                    active: True if app.config.get('CustSettings', 'Mode') == 'Dark'\
                            else False
            FloatLayout:
                size_hint_y: None
                height : currency.size[1]   
                pos_hint: {'x': 0, 'y': .61} 
                MDLabel:
                    size_hint_x: .4
                    pos_hint: {'x': .05, 'y': .05}                
                    text: 'Activate Daily Limit'
                    halign: 'left'                    
                    theme_text_color: "Primary"
                MDSwitch:
                    id: dailylimit
                    size_hint_x: .1
                    pos_hint: {'x': .52, 'y': .05}  
                    on_active: root.daily_limit()
                    active: True if app.config.get('CustSettings', 'DayLimitFlg') == 'True'\
                            else False  
            FloatLayout:
                size_hint_y: None
                height : currency.size[1]
                pos_hint: {'x': 0, 'y': .50}    
                canvas.before:
                    Color:
                        rgba: app.theme_cls.divider_color
                    Line:
                        width: .5
                        points: [self.x + 5, self.y, self.x - 5 + self.width, self.y ]                
                MDLabel:
                    size_hint_x: .4
                    pos_hint: {'x': .05, 'y': .05}                
                    text: 'Daily Limit Amount'
                    halign: 'left'                    
                    theme_text_color: "Primary"
                MDTextField:
                    id: dlimitamt
                    size_hint_x: .4
                    pos_hint: {'x': .5, 'y': .05}  
                    normal_color: app.theme_cls.accent_light
                    foreground_color : app.theme_cls.text_color
                    elevation: 10
                    input_filter : 'float'       
                    on_text: root.update_setting()   
                    theme_text_color: "Primary"           


<CustomDropDown>:
    padding: 1
    MDRectangleFlatButton:
        text: '₹'
        size_hint_x: None
        width: root.width
        on_release: root.select('₹')
        md_bg_color : app.theme_cls.accent_light
    MDRectangleFlatButton:
        text: '$'
        size_hint_x: None
        width: root.width          
        on_release: root.select('$')
        md_bg_color : app.theme_cls.accent_light
    MDRectangleFlatButton:
        text: '€'
        size_hint_x: None
        width: root.width          
        on_release: root.select('€')
        md_bg_color : app.theme_cls.accent_light
    MDRectangleFlatButton:
        text: '£'
        size_hint_x: None
        width: root.width          
        on_release: root.select('£')
        md_bg_color : app.theme_cls.accent_light
    MDRectangleFlatButton:
        text: '¥'
        size_hint_x: None
        width: root.width          
        on_release: root.select('¥')
        md_bg_color : app.theme_cls.accent_light
'''


class CustomDropDown(DropDown):
    pass


class CustomLabel(MDLabel, ButtonBehavior):
    pass


class SettingsPage(Screen):
    def __init__(self, **kwargs):
        self.name = 'Settings'
        global app_scr
        app_scr = kwargs['app']
        super(SettingsPage, self).__init__()
        self.dropdown = CustomDropDown()
        self.ids.currency.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: self.set_currency(x))
        self.ids.currency.text = app_scr.config.get('CustSettings', 'Currency')
        self.ids.dlimitamt.text = app_scr.config.get('CustSettings', 'DayLimitAmt')
        if app_scr.config.get('CustSettings', 'DayLimitFlg') == 'False':
            self.ids.dlimitamt.disabled = True

    def set_currency(self, text):
        self.ids.currency.text = text
        app_scr.config.set('CustSettings', 'Currency', text)
        app_scr.config.write()

    def dark_mode(self):
        if self.ids.darkmode.active:
            app_scr.theme_cls.theme_style = 'Dark'
        else:
            app_scr.theme_cls.theme_style = 'Light'

        app_scr.config.set('CustSettings', 'Mode', app_scr.theme_cls.theme_style)
        app_scr.config.write()

    def daily_limit(self):
        if self.ids.dailylimit.active:
            self.ids.dlimitamt.disabled = False
        else:
            self.ids.dlimitamt.disabled = True

        app_scr.config.set('CustSettings', 'DayLimitFlg', self.ids.dailylimit.active)
        app_scr.config.write()

    def update_setting(self):
        if self.ids.dlimitamt.text == '' or self.ids.dlimitamt.text is None:
            self.ids.dlimitamt.text = '0'
        limit = float(self.ids.dlimitamt.text)
        app_scr.config.set('CustSettings', 'DayLimitAmt', limit)
        app_scr.config.write()

