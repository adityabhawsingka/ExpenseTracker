from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from datetime import date
from kivymd.cards import MDCard
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from dtclasses import Expenses, Items


class CardButton(ButtonBehavior, MDCard):
    fixed_size = (0, 0)
    fixed_pos = (0, 0)

    def __init__(self, **kwargs):
        super(CardButton, self).__init__(**kwargs)

    def on_press(self):
        self.fade_bg = Animation(duration=.25,
                                 md_bg_color=app_scr.theme_cls.accent_color,
                                 size_hint_x=self.fixed_size[0] - .1,
                                 pos_hint={'x': self.fixed_pos[0] + 0.05, 'y': self.fixed_pos[1]})
        self.fade_bg.start(self)

        # self.fade_bg = Animation(duration=.5, md_bg_color=current_bg_color)
        # self.fade_bg.start(self)

    def on_release(self):
        self.fade_bg.stop(self)
        self.fade_bg = Animation(duration=.25, md_bg_color=app_scr.theme_cls.bg_light,
                                 size_hint_x=self.fixed_size[0],
                                 pos_hint={'x': self.fixed_pos[0], 'y': self.fixed_pos[1]})
        self.fade_bg.start(self)
        app_scr.screens.show_screen('Expenses')


dashboard = '''
#:import MDFlatButton kivymd.button.MDFlatButton
#:import MDLabel kivymd.label.MDLabel

<Dashboard>:
    FloatLayout:
        CardButton:
            fixed_size: (.95, .279)
            size_hint : (.95, .279)
            fixed_pos : (.025, .70)
            pos_hint : {'x' : .025, 'y' : .70}
            elevation : 10     
            border_radius: 10
            FloatLayout:
                FloatLayout:
                    size_hint : (1, .35)
                    pos_hint: {'x': 0 ,'y':.65} 
                    canvas.before:
                        Color:
                            rgba: app.theme_cls.primary_color
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [(10, 10), (10, 10), (0,0), (0,0)]
                    MDLabel:
                        size_hint: (.3, 1)
                        pos_hint: {'x': 0,'y': 0} 
                        theme_text_color: 'Primary'
                        text : 'DAY'
                        halign : 'center'
                        canvas.before:
                            Color:
                                rgba: app.theme_cls.primary_color
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [(10, 10), (0, 0), (0,0), (0,0)] 
                                                        
                    MDLabel:
                        id : lbl_day_date
                        size_hint: (.7, 1)
                        pos_hint: {'x': .3,'y': 0} 
                        theme_text_color: 'Primary'
                        halign : 'center'
                        canvas.before:
                            Color:
                                rgba: app.theme_cls.primary_light
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [(0, 0), (10, 10), (0,0), (20,20)] 
                FloatLayout:
                    pos_hint: {'x': .0 ,'y': .0}
                    size_hint : (1, .65)                
                    MDLabel:
                        id : lbl_day_total
                        font_style : 'H3'
                        theme_text_color : 'Secondary'
                        halign : 'center'
                        pos_hint: {'x': 0 ,'y': 0}  
        CardButton:
            size_hint : (.95, .279)
            pos_hint : {'x' : .025, 'y' : .38}
            elevation : 10     
            fixed_size: (.95, .279)
            fixed_pos : (.025, .38)
            border_radius: 10
            FloatLayout:
                FloatLayout:
                    size_hint : (1, .35)
                    pos_hint: {'x': 0 ,'y':.65} 
                    canvas.before:
                        Color:
                            rgba: app.theme_cls.primary_color
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [(10, 10), (10, 10), (0,0), (0,0)]
                    MDLabel:
                        size_hint: (.3, 1)
                        pos_hint: {'x': 0,'y': 0} 
                        theme_text_color: 'Primary'
                        text : 'MONTH'
                        halign : 'center'
                        canvas.before:
                            Color:
                                rgba: app.theme_cls.primary_color
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [(10, 10), (0, 0), (0,0), (0,0)] 
                                                        
                    MDLabel:
                        id : lbl_month_date
                        size_hint: (.7, 1)
                        pos_hint: {'x': .3,'y': 0} 
                        theme_text_color: 'Primary'
                        halign : 'center'
                        canvas.before:
                            Color:
                                rgba: app.theme_cls.primary_light
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [(0, 0), (10, 10), (0,0), (20,20)] 
                FloatLayout:
                    pos_hint: {'x': .0 ,'y': .0}
                    size_hint : (1, .65)                
                    MDLabel:
                        id : lbl_month_total
                        font_style : 'H3'
                        theme_text_color : 'Secondary'
                        halign : 'center'
                        pos_hint: {'x': 0 ,'y': 0}  
                                                                
        CardButton:
            size_hint : (.95, .279)
            pos_hint : {'x' : .025, 'y' : .06}
            elevation : 10            
            fixed_size: (.95, .279)
            fixed_pos : (.025, .06)
            elevation : 10     
            border_radius: 10
            FloatLayout:
                FloatLayout:
                    size_hint : (1, .35)
                    pos_hint: {'x': 0 ,'y':.65} 
                    canvas.before:
                        Color:
                            rgba: app.theme_cls.primary_color
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [(10, 10), (10, 10), (0,0), (0,0)]
                    MDLabel:
                        size_hint: (.3, 1)
                        pos_hint: {'x': 0,'y': 0} 
                        theme_text_color: 'Primary'
                        text : 'YEAR'
                        halign : 'center'
                        canvas.before:
                            Color:
                                rgba: app.theme_cls.primary_color
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [(10, 10), (0, 0), (0,0), (0,0)] 
                                                        
                    MDLabel:
                        id : lbl_year_date
                        size_hint: (.7, 1)
                        pos_hint: {'x': .3,'y': 0} 
                        theme_text_color: 'Primary'
                        halign : 'center'
                        canvas.before:
                            Color:
                                rgba: app.theme_cls.primary_light
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [(0, 0), (10, 10), (0,0), (20,20)] 
                FloatLayout:
                    pos_hint: {'x': .0 ,'y': .0}
                    size_hint : (1, .65)                
                    MDLabel:
                        id : lbl_year_total
                        font_style : 'H3'
                        theme_text_color : 'Secondary'
                        halign : 'center'
                        pos_hint: {'x': 0 ,'y': 0}  
            
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: .003
            canvas.before:
                Color:
                    rgba: app.theme_cls.primary_color
                Rectangle:
                    size: self.size
                    pos: self.pos 
            MDFloatingActionButton:
                pos_hint: {'center_x': .5, 'center_y': .5}
                icon: 'plus'
                opposite_colors: True
                elevation_normal: 10
                on_release: root.add_expense()          

'''


class Dashboard(Screen):
    display_date = ObjectProperty()
    current_date = date.today()

    def __init__(self, **kwargs):
        global app_scr
        app_scr = kwargs['app']
        self.name = 'Dashboard'
        super(Dashboard, self).__init__()
        self.ids.lbl_day_date.text = self.current_date.strftime('%d %b %Y')
        self.ids.lbl_month_date.text = self.current_date.strftime('%b %Y')
        self.ids.lbl_year_date.text = self.current_date.strftime('%Y')
        Items.data_correction()

    def on_enter(self, *args):
        self.update_totals()

    def update_totals(self):
        currency = app_scr.config.get('CustSettings', 'Currency')
        totals = Expenses.get_totals(self.current_date)
        self.ids.lbl_day_total.text = '{} {}'.format(currency, str(totals['day']))
        self.ids.lbl_month_total.text = '{} {}'.format(currency, str(totals['month']))
        self.ids.lbl_year_total.text = '{} {}'.format(currency, str(totals['year']))

        day_limit = float(app_scr.config.get('CustSettings', 'DayLimitAmt'))
        day_limit_flg = app_scr.config.get('CustSettings', 'DayLimitFlg')
        if totals['day'] > day_limit and day_limit_flg == 'True':
            app_scr.theme_cls.primary_palette = 'Red'
        else:
            app_scr.theme_cls.primary_palette = 'Teal'

    def add_expense(self):
        app_scr.date = self.current_date.strftime('%Y-%m-%d')
        app_scr.screens.show_screen('Add Expense')

