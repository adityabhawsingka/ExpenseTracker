from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty

from kivymd.label import MDLabel
from kivymd.list import OneLineRightIconListItem, IRightBody
from kivymd.tabs import MDTabsBase
from kivymd.pickers import MDDatePicker
from kivymd.button import MDIconButton

from kivytoast import Toast
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

from dtclasses import Expenses
from monthpicker import MDMonthPicker

expdetail_obj = ObjectProperty()

dashboard2 = """
#:import MDLabel kivymd.label.MDLabel
#:import MDList kivymd.list.MDList
#:import MDDatePicker kivymd.pickers.MDDatePicker
#:import MDBottomAppBar kivymd.toolbar.MDBottomAppBar
#:import MDTextFieldRound kivymd.textfields.MDTextFieldRound
#:import MDTabs kivymd.tabs.MDTabs

<Dashboard2@Screen>
    orientation: 'vertical'
    android_tabs : android_tabs.__self__
    MDTabs:
        id: android_tabs
        tab_indicator_anim : True
        anim_duration : 0.1

<DayTab>:
    orientation: 'vertical'
    daytab : daytab.__self__
    BoxLayout:
        id: daytab
        orientation: 'horizontal'
        size_hint_y: .12
        canvas.before:
            Color:
                rgba: app.theme_cls.primary_light
            Rectangle:
                size: self.size
                pos: self.pos        
        MDIconButton:
            icon: 'chevron-left'
            size_hint_x: .15
            on_press: root.left_arrow()
        MDLabel:
            id: datelabel
            size_hint_x: .55
            on_text: root.refresh_list()
            halign : 'center'
            theme_text_color: "Primary"
        MDIconButton:
            icon: 'chevron-right'
            size_hint_x: .15
            on_press: root.right_arrow()
        MDIconButton:
            icon: 'calendar'
            size_hint_x: .15
            on_press: root.show_date_picker()                 

    ScrollView:
        do_scroll_x : False
        size_hint_y: .75
        bar_width: 5
        MDList:
            id: list
            
    BoxLayout:
        size_hint_y: .125
        canvas.before:
            Color:
                rgba: app.theme_cls.primary_light
            Rectangle:
                size: self.size
                pos: self.pos 
        BoxLayout:
            size_hint_x: .05       
        MDLabel:
            text: 'Total'
            size_hint_x: .55
            theme_text_color: "Primary"
        MDLabel:
            id: total
            halign : 'right'
            size_hint_x: .35
            theme_text_color: "Primary"
        BoxLayout:
            size_hint_x: .05   

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: .005
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


<MonthTab>:
    orientation: 'vertical'
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: .12
        canvas.before:
            Color:
                rgba: app.theme_cls.primary_light
            Rectangle:
                size: self.size
                pos: self.pos        
        MDIconButton:
            icon: 'chevron-left'
            size_hint_x: .15
            on_press: root.left_arrow()
        MDLabel:
            id: monthlabel
            size_hint_x: .55
            halign : 'center'
            on_text: root.refresh_list()
            theme_text_color: "Primary"
        MDIconButton:
            icon: 'chevron-right'
            size_hint_x: .15
            on_press: root.right_arrow()
        MDIconButton:
            icon: 'calendar'
            size_hint_x: .15
            on_press: root.show_month_picker()     

    ScrollView:
        do_scroll_x : False
        size_hint_y: .75
        bar_width: 5
        MDList:
            id: monthlist
        

    BoxLayout:
        size_hint_y: .125
        canvas.before:
            Color:
                rgba: app.theme_cls.primary_light
            Rectangle:
                size: self.size
                pos: self.pos 
        BoxLayout:
            size_hint_x: .05       
        MDLabel:
            text: 'Total'
            size_hint_x: .55
            theme_text_color: "Primary"
        MDLabel:
            id: total
            halign : 'right'
            size_hint_x: .35
            theme_text_color: "Primary"
        BoxLayout:
            size_hint_x: .05



<YearTab>:
    orientation: 'vertical'
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: .12
        canvas.before:
            Color:
                rgba: app.theme_cls.primary_light
            Rectangle:
                size: self.size
                pos: self.pos        
        MDIconButton:
            icon: 'chevron-left'
            size_hint_x: .2
            on_press: root.left_arrow()
        MDLabel:
            id: yearlabel
            size_hint_x: .6
            halign : 'center'
            on_text: root.refresh_list()
            theme_text_color: "Primary"
        MDIconButton:
            icon: 'chevron-right'
            size_hint_x: .2
            on_press: root.right_arrow()    

    ScrollView:
        do_scroll_x : False
        size_hint_y: .75
        bar_width: 5
        MDList:
            id: yearlist


    BoxLayout:
        size_hint_y: .125
        canvas.before:
            Color:
                rgba: app.theme_cls.primary_light
            Rectangle:
                size: self.size
                pos: self.pos 
        BoxLayout:
            size_hint_x: .05       
        MDLabel:
            text: 'Total'
            size_hint_x: .55
            theme_text_color: "Primary"
        MDLabel:
            id: total
            halign : 'right'
            size_hint_x: .35
            theme_text_color: "Primary"
        BoxLayout:
            size_hint_x: .05      


"""


class ListRightBox(IRightBody, BoxLayout):
    """Class to create a label which will added to right side of day tab list"""
    expense_id = NumericProperty(0)

    def __init__(self, **kwargs):
        super(ListRightBox, self).__init__()
        self.expense_id = kwargs['expense_id']
        self.add_widget(MDLabel(text=kwargs['right_text'],
                                halign='right',
                                theme_text_color='Primary',
                                size_hint_x=.9))
        self.add_widget(MDIconButton(icon='delete-outline',
                                     size_hint_x=.1,
                                     on_release=self.on_release))

    def on_release(self, *args):
        Expenses.del_expense(expense_id=self.expense_id)
        expdetail_obj.daytab.refresh_list()
        expdetail_obj.yeartab.refresh_list()
        expdetail_obj.monthtab.refresh_list()
        Toast(opacity=0.5).toast('Expense Deleted')


class ListRightLabel(IRightBody, MDLabel):
    """Class to create a label which will added to right side of day tab list"""

    def __init__(self, **kwargs):
        self.text = kwargs['right_text']
        self.halign = 'right'
        self.theme_text_color = "Primary"
        super(ListRightLabel, self).__init__()


class CustomDayItem(OneLineRightIconListItem):
    """Class to create a list item on the day tab screen"""

    def __init__(self, **kwargs):
        self.text = kwargs['text']
        super(CustomDayItem, self).__init__()
        self.ids._right_container.size_hint_x = .5
        self.add_widget(ListRightBox(**kwargs))


class CustomListItem(OneLineRightIconListItem):
    """Class to create a list item on the day tab screen"""

    def __init__(self, **kwargs):
        self.text = kwargs['text']
        super(CustomListItem, self).__init__()
        self.ids._right_container.size_hint_x = .5
        self.add_widget(ListRightLabel(**kwargs))


class DayTab(BoxLayout, MDTabsBase):
    display_date = ObjectProperty()
    current_date = date.today()

    def __init__(self, **kwargs):
        super(DayTab, self).__init__(**kwargs)
        self.display_date = self.ids.datelabel
        self.display_date.text = self.current_date.strftime('%d %b %Y')

    def show_date_picker(self):
        MDDatePicker(self.pick_date).open()

    def pick_date(self, date_selected):
        self.current_date = date_selected
        self.display_date.text = self.current_date.strftime('%d %b %Y')

    def refresh_list(self):
        self.ids.list.clear_widgets()
        currency = app_scr.config.get('CustSettings', 'Currency')
        expense_dict = Expenses.get_expenses(date=self.current_date.strftime('%Y-%m-%d'), date_type='day')
        if expense_dict == {}:
            self.ids.list.add_widget(MDLabel(text='No expenses to show',
                                             halign='center',
                                             theme_text_color='Hint'))
        total = 0.0
        for key, value in expense_dict.items():
            self.ids.list.add_widget(CustomDayItem(text=value['item_name'],
                                                   right_text='{} {}'.format(currency, str(value['value'])),
                                                   expense_id=key))
            total = total + value['value']
        self.ids.total.text = '{} {}'.format(currency, total)

    def add_expense(self):
        app_scr.date = self.current_date.strftime('%Y-%m-%d')
        app_scr.screens.show_screen('Add Expense')

    def left_arrow(self):
        self.current_date = self.current_date - timedelta(days=1)
        self.display_date.text = self.current_date.strftime('%d %b %Y')

    def right_arrow(self):
        self.current_date = self.current_date + timedelta(days=1)
        self.display_date.text = self.current_date.strftime('%d %b %Y')


class MonthTab(BoxLayout, MDTabsBase):
    current_date = date.today()
    display_date = ObjectProperty()

    def __init__(self, **kwargs):
        super(MonthTab, self).__init__(**kwargs)
        self.display_date = self.ids.monthlabel
        self.display_date.text = self.current_date.strftime('%b %Y')

    def refresh_list(self):
        self.ids.monthlist.clear_widgets()
        currency = app_scr.config.get('CustSettings', 'Currency')
        expense_dict = Expenses.get_expenses(date=self.current_date, date_type='month')
        if expense_dict == {}:
            self.ids.monthlist.add_widget(MDLabel(text='No expenses to show',
                                                  halign='center',
                                                  theme_text_color='Hint'))
        total = 0.0
        for key, value in expense_dict.items():
            exp_date = datetime.strptime(key, '%Y-%m-%d')
            self.ids.monthlist.add_widget(CustomListItem(text=exp_date.strftime('%d %b %Y'),
                                                         right_text='{} {}'.format(currency, str(value))))
            total = total + value
        self.ids.total.text = '{} {}'.format(currency, total)

    def show_month_picker(self):
        MDMonthPicker(self.pick_month).open()

    def pick_month(self, year, month):
        self.current_date = self.current_date.replace(month=month, year=year)
        self.display_date.text = self.current_date.strftime('%b %Y')

    def left_arrow(self):
        self.current_date = self.current_date - relativedelta(months=1)
        self.display_date.text = self.current_date.strftime('%b %Y')

    def right_arrow(self):
        self.current_date = self.current_date + relativedelta(months=1)
        self.display_date.text = self.current_date.strftime('%b %Y')


class YearTab(BoxLayout, MDTabsBase):
    current_date = date.today()
    display_date = ObjectProperty()
    year = None

    def __init__(self, **kwargs):
        super(YearTab, self).__init__(**kwargs)
        self.display_date = self.ids.yearlabel
        self.display_date.text = self.current_date.strftime('%Y')
        self.refresh_list()

    def refresh_list(self):
        self.ids.yearlist.clear_widgets()
        currency = app_scr.config.get('CustSettings', 'Currency')
        expense_dict = Expenses.get_expenses(date=self.current_date, date_type='year')
        if expense_dict == {}:
            self.ids.yearlist.add_widget(MDLabel(text='No expenses to show',
                                                 halign='center',
                                                 theme_text_color='Hint'))
        total = 0.0
        for key, value in expense_dict.items():
            self.ids.yearlist.add_widget(CustomListItem(text=key,
                                                        right_text='{} {}'.format(currency, str(value))))
            total = total + float(value)
        self.ids.total.text = '{} {}'.format(currency, total)

    def left_arrow(self):
        self.current_date = self.current_date - relativedelta(years=1)
        self.display_date.text = self.current_date.strftime('%Y')

    def right_arrow(self):
        self.current_date = self.current_date + relativedelta(years=1)
        self.display_date.text = self.current_date.strftime('%Y')


class Dashboard2(BoxLayout, Screen):
    def __init__(self, **kwargs):
        self.name = 'Dashboard2'
        super(Dashboard2, self).__init__()
        global app_scr, expdetail_obj
        app_scr = kwargs['app']
        expdetail_obj = self

        self.daytab = DayTab(text='Day')
        self.ids.android_tabs.add_widget(self.daytab)

        self.monthtab = MonthTab(text='Month')
        self.ids.android_tabs.add_widget(self.monthtab)

        self.yeartab = YearTab(text='Year')
        self.ids.android_tabs.add_widget(self.yeartab)

    def on_enter(self, *args):
        self.daytab.refresh_list()
        self.monthtab.refresh_list()
        self.yeartab.refresh_list()

    def on_leave(self, *args):
        self.yeartab.ids.yearlist.clear_widgets()
        self.monthtab.ids.monthlist.clear_widgets()
        self.daytab.ids.list.clear_widgets()
