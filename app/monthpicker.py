"""
Pickers
=======

Copyright (c) 2015 Andrés Rodríguez and KivyMD contributors -
    KivyMD library up to version 0.1.2
Copyright (c) 2019 Ivanov Yuri and KivyMD contributors -
    KivyMD library version 0.1.3 and higher

For suggestions and questions:
<kivydevelopment@gmail.com>

This file is distributed under the terms of the same license,
as the Kivy framework.

Includes date, time and color picker
"""

import calendar
from datetime import date

from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, NumericProperty, ObjectProperty,\
    BooleanProperty, ListProperty, OptionProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

from kivymd.label import MDLabel
from kivymd.button import MDIconButton
from kivymd.theming import ThemableBehavior
from kivymd.backgroundcolorbehavior import SpecificBackgroundColorBehavior
from kivymd.ripplebehavior import CircularRippleBehavior
from kivymd.elevation import RectangularElevationBehavior
from kivymd.color_definitions import colors, palette


Builder.load_string('''
#:import calendar calendar
#:import platform platform


<MDMonthPicker>
    cal_layout: cal_layout
    size_hint: (.8, .5)
    pos_hint: {'center_x': .5, 'center_y': .5}
    canvas:
        Color:
            rgb: root.theme_cls.bg_normal
        Rectangle:
            size: self.size
            pos: self.pos   

    GridLayout:
        id: cal_layout
        cols: 3
        canvas:
            Color:
                rgb: root.theme_cls.bg_light
            Rectangle:
                size: self.size
                pos: self.pos         
        size_hint: (1, .6)
        pos_hint: {'x': 0, 'y': .2}

    MDLabel:
        id: label_month_selector
        canvas.before:
            Color:
                rgba:root.theme_cls.primary_color
            Rectangle:
                size: self.size
                pos: self.pos
        font_style: 'Subtitle1'  
        text: str(root.year)
        size_hint: (.7,.2)
        theme_text_color: 'Primary'
        pos_hint: {'center_x': .5, 'center_y': .9}
        valign: "middle"
        halign: "center"

    MDIconButton:
        icon: 'chevron-left'
        canvas.before:
            Color:
                rgba:root.theme_cls.primary_color
            Rectangle:
                size: self.size
                pos: self.pos
        font_style: 'Subtitle1'         
        theme_text_color: 'Secondary'
        size_hint:(.15, .2)
        pos_hint: {'center_x': .075, 'center_y': .9}
        on_release: root.change_year('prev')

    MDIconButton:
        icon: 'chevron-right'
        canvas.before:
            Color:
                rgba:root.theme_cls.primary_color
            Rectangle:
                size: self.size
                pos: self.pos
        font_style: 'Subtitle1'         
        theme_text_color: 'Secondary'
        size_hint:(.15, .2)
        pos_hint: {'center_x': .925, 'center_y': .9}
        on_release: root.change_year('next')
        
    FloatLayout:
        size_hint: (1,.2)
        pos_hint: {'x': 0, 'y': 0}
        canvas.before:
            Color:
                rgba:root.theme_cls.primary_light
            Rectangle:
                size: self.size
                pos: self.pos    
        MDFlatButton:
            id: ok_button
            size_hint: (.2,1)
            pos_hint: {'x': .8, 'y': 0}
            text: "OK"
            on_release: root.ok_click()
        MDFlatButton:
            id: cancel_button
            size_hint: (.2,1)
            pos_hint: {'x': .6, 'y': 0}
            text: "Cancel"
            on_release: root.dismiss()


<MonthButton>
    back_color: root.theme_cls.bg_normal
    size_hint: (.33, .25)
    canvas.before:
        Color:
            rgba: self.back_color
        Rectangle:
            size: self.size
            pos: self.pos
    MDLabel:
        id: monthlabel
        lbl_back_color: self.theme_cls.bg_dark         
        canvas.before:
            Color:
                rgba: 
                    self.lbl_back_color if self.lbl_back_color is not None\
                    else self.theme_cls.bg_dark
            Rectangle:
                size: self.size
                pos: self.pos    
        font_style: 'Caption'
        theme_text_color: 'Primary'
        size_hint: (.95, .95)
        valign: 'middle'
        halign: 'center'
        text: root.text
''')


class MonthButton(ThemableBehavior, CircularRippleBehavior, ButtonBehavior,
                AnchorLayout):
    text = StringProperty()
    owner = ObjectProperty()
    is_current_month = BooleanProperty(False)
    is_selected = BooleanProperty(False)
    back_color = ObjectProperty()

    def on_release(self):
        self.owner.set_selected_widget(self)


class MDMonthPicker(FloatLayout, ThemableBehavior, RectangularElevationBehavior,
                   SpecificBackgroundColorBehavior, ModalView):
    _sel_month_widget = ObjectProperty()
    cal_list = None
    cal_layout = ObjectProperty()
    sel_year = NumericProperty()
    sel_month = NumericProperty()
    sel_day = NumericProperty()
    day = NumericProperty()
    month = NumericProperty()
    year = NumericProperty()
    today = date.today()
    callback = ObjectProperty()
    background_color = ListProperty([0, 0, 0, .7])
    month_list = [calendar.month_abbr[x] for x in range(1, 13)]

    class SetDateError(Exception):
        pass

    def __init__(self, callback, year=None, month=None, day=None,
                 firstweekday=0, **kwargs):
        self.callback = callback
        self.cal = calendar.Calendar(firstweekday)
        self.sel_year = year if year else self.today.year
        self.sel_month = month if month else self.today.month
        self.sel_day = day if day else self.today.day
        self.month = self.sel_month
        self.year = self.sel_year
        self.day = self.sel_day
        super().__init__(**kwargs)
        self.generate_cal_widgets()

    def change_year(self, operation):
        op = 1 if operation is 'next' else -1
        sy = self.year
        y = sy + op
        self.sel_year = y
        self.year = y

    def generate_cal_widgets(self):
        cal_list = []
        for i in range(12):
            mb = MonthButton(owner=self, text=self.month_list[i], back_color=self.theme_cls.bg_normal)
            cal_list.append(mb)
            self.cal_layout.add_widget(mb)
        self.cal_list = cal_list

    def set_selected_widget(self, widget):
        if self._sel_month_widget is not None:
            self._sel_month_widget.back_color = self.theme_cls.bg_normal
            self._sel_month_widget.ids.monthlabel.lbl_back_color = self.theme_cls.bg_dark
            # self._sel_month_widget.ids.monthlabel.theme_text_color = 'Primary'
        widget.is_selected = True
        widget.back_color = self.theme_cls.bg_darkest
        widget.ids.monthlabel.lbl_back_color = self.theme_cls.bg_darkest
        self.sel_month = self.month_list.index(widget.text) + 1
        self.sel_year = int(self.year)
        self._sel_month_widget = widget
        self.month = self.sel_month
        self.year = self.sel_year

    def ok_click(self):
        self.callback(self.sel_year, self.sel_month)
        self.dismiss()



if __name__ == "__main__":
    from kivy.app import App
    from kivymd.theming import ThemeManager
    from kivy.uix.boxlayout import BoxLayout
    from kivymd.button import MDRaisedButton
    from kivy.lang import Builder

    Builder.load_string('''
#:import MDRaisedButton kivymd.button.MDRaisedButton
    
<Mpicker@BoxLayout>
    MDRaisedButton:
        on_release : root.show_date_picker()
    ''')

    class Mpicker(BoxLayout):

        def __init__(self):
            super(Mpicker, self).__init__()
            #self.add_widget(MDRaisedButton(on_release=self.show_date_picker))

        def show_date_picker(self):
            #MDDatePicker(self.pick_date).open()
            MDMonthPicker(self.pick_date).open()

        def pick_date(self, year, month):
            print(year,month)

            # self.current_date = date_selected
            # self.display_date.text = self.current_date.strftime('%Y-%m-%d')

    class MonthPicker(App):
        theme_cls = ThemeManager()
        theme_cls.primary_palette = 'BlueGray'
        theme_cls.accent_palette = 'Gray'

        def build(self):

            return Mpicker()



    MonthPicker().run()
