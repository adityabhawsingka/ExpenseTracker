from datetime import datetime, timedelta

from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.app import App

from kivymd.pickers import MDDatePicker

from kivytoast import toast
from dtclasses import Items, Expenses
from additem import CustomFlatButton

add_expense = """
#:import MDTextField kivymd.textfields.MDTextField
<AddExpense>
    item_name: item_name.__self__
    value: value.__self__
    submit: submit.__self__
    lbl_message: lbl_message.__self__
    datelabel : datelabel.__self__
    daycalendar: daycalendar.__self__
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: .1
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
                #on_text: root.refresh_list()
                halign : 'center'
                theme_text_color: "Primary"
            MDIconButton:
                icon: 'chevron-right'
                size_hint_x: .15
                on_press: root.right_arrow()
            MDIconButton:
                id: daycalendar
                icon: 'calendar'
                size_hint_x: .15
                on_press: root.show_date_picker()          
        FloatLayout:
            # orientation: 'vertical'
            size_hint_y : .7
            MDTextField:
                id: item_name
                # pos_hint: {'center_x': .5}
                hint_text: 'Category/Sub-Category'  
                size_hint_x : .75
                pos_hint: {'x': .1, 'y': .75}
                normal_color: app.theme_cls.accent_light
                foreground_color : app.theme_cls.text_color
                on_text: root.get_category('field')
                elevation: 10
                helper_text_mode : 'on_focus'
                helper_text : 'Type/Select from Dropdown'
                input_filter: root.text_filter
                max_text_length: 20
            MDIconButton:
                icon: 'chevron-down'
                size_hint_x: .15
                pos_hint: {'x': .85, 'y': .75}
                on_release: root.get_category('button')
            MDTextField:
                id: value
                size_hint_x : .75
                pos_hint: {'x': .1, 'y': .55}                    
                hint_text: 'Value'  
                normal_color: app.theme_cls.accent_light
                foreground_color : app.theme_cls.text_color
                elevation: 10
                input_filter : 'float'   
                helper_text_mode : 'on_focus'
                helper_text : 'Enter expense amount'                          
            MDFillRoundFlatButton:
                id: submit
                pos_hint: {'x': .1, 'y': .3}
                size_hint_x: .75
                # width: 250
                text: 'Submit'
                on_release: root.add_expense() 
            MDLabel:
                id: lbl_message   
                size_hint_x: .8
                pos_hint: {'center_x': .5, 'center_y': .2}    
                halign: 'center'  
                theme_text_color: "Primary"                      
        BoxLayout:
            size_hint_y : .2

"""


class AddExpense(Screen):
    expense_date = datetime.today()
    cat_dropdown = DropDown()

    def __init__(self, **kwargs):
        self.name = "Add Expense"
        self.app = App.get_running_app()
        super(AddExpense, self).__init__()
        self.cat_dropdown.bind(
            on_select=lambda instance, x: setattr(self.item_name, "text", x)
        )
        self.cat_dropdown.width = self.item_name.width

    def show_date_picker(self):
        MDDatePicker(self.pick_date).open()

    def pick_date(self, exp_date):
        self.lbl_message.text = ""
        self.datelabel.text = str(exp_date)
        self.expense_date = exp_date

    def add_expense(self):
        item_name = self.item_name.text
        value = self.value.text
        exp_date = self.datelabel.text

        if (
            item_name is None
            or item_name == ""
            or value is None
            or value == ""
            or exp_date is None
            or exp_date == ""
        ):
            self.lbl_message.text = "Required input missing."
            self.lbl_message.theme_text_color = "Error"
            return

        item_id = Items.get_item(item_name=item_name, item_link=None)
        if item_id is None or item_id == 0:
            self.lbl_message.text = (
                "No Category/Sub-Category by this name. "
                "Please create if required from Items screen."
            )
            self.lbl_message.theme_text_color = "Error"
            return

        if value == "0":
            self.lbl_message.text = "Enter an amount not equal to 0"
            self.lbl_message.theme_text_color = "Error"
            return

        expense_id = Expenses.get_next_exp_id()

        kwargs = {
            "expense_id": expense_id,
            "item_id": item_id,
            "value": float(value),
            "date": exp_date,
        }

        Expenses.add_expense(**kwargs)

        toast("Expense Added")
        self.leave_screen()

    def on_enter(self, *args):
        self.expense_date = datetime.strptime(self.app.date, "%Y-%m-%d")
        self.datelabel.text = self.app.date
        self.item_name.text = ""
        self.value.text = ""
        self.item_name.focus = True
        self.lbl_message.text = ""

    def left_arrow(self):
        self.expense_date = self.expense_date - timedelta(days=1)
        self.datelabel.text = self.expense_date.strftime("%Y-%m-%d")
        self.lbl_message.text = ""

    def right_arrow(self):
        self.expense_date = self.expense_date + timedelta(days=1)
        self.datelabel.text = self.expense_date.strftime("%Y-%m-%d")
        self.lbl_message.text = ""

    def get_category(self, *args):
        """function to get items based on the search text entered by user"""
        self.cat_dropdown.clear_widgets()
        self.lbl_message.text = ""
        if self.cat_dropdown.attach_to is not None:
            self.cat_dropdown._real_dismiss()
        item_name = self.item_name.text
        item_dict = {}
        if item_name is not None and item_name != "" and args[0] != "button":
            item_dict = Items.get_items(item_name=item_name, item_type="all")
        if args[0] == "button":
            item_dict = Items.get_items(item_name="", item_type="all")
        if item_dict != {}:
            for key, value in item_dict.items():
                self.cat_dropdown.add_widget(
                    CustomFlatButton(
                        text=value["item_name"],
                        on_release=lambda x: self.cat_dropdown.select(x.text),
                        md_bg_color=self.app.theme_cls.accent_light,
                        width=self.item_name.width,
                    )
                )

            self.cat_dropdown.open(self.item_name)

    def text_filter(self, input_text, undo_flag):
        if input_text.isalnum():
            return input_text
        else:
            return

    def leave_screen(self, *args):
        self.app.screens.show_screen("Expenses")

    def on_leave(self, *args):
        self.cat_dropdown.clear_widgets()
