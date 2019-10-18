from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown

from kivymd.button import MDRectangleFlatButton

from dtclasses import Items
from kivytoast import toast

additem = '''
#:import MDTextField kivymd.textfields.MDTextField
#:import MDLabel kivymd.label.MDLabel
#:import MDCheckbox kivymd.selectioncontrols.MDCheckbox
#:import MDFillRoundFlatButton kivymd.button.MDFillRoundFlatButton

<AddItem>
    FloatLayout:
        MDLabel:
            id: lbl_item_type
            halign: 'center'
            theme_text_color: 'Primary'
            size_hint : (.5, .1)
            pos_hint: {'x': .25, 'y': .85}            
        MDTextField:
            id: category
            hint_text: 'Category'
            size_hint_x : .75
            pos_hint: {'x': .1, 'y': .7}
            #focus: True
            elevation: 10
            on_text: root.get_category('field') 
            foreground_color : app.theme_cls.text_color
            # pos_hint: {'center_x': .5}
            normal_color: app.theme_cls.accent_light
            require_text_error : 'This field is required'
            helper_text_mode: 'on_focus'
            max_text_length: 20
            input_filter: root.text_filter
        MDIconButton:
            id: drop_button
            icon: 'chevron-down'
            size_hint_x: .15
            pos_hint: {'x': .85, 'y': .7}
            on_release: root.get_category('button')                  
        MDTextField:
            id: subcategory
            hint_text: 'Sub-Category'
            elevation: 10
            size_hint_x : .75
            pos_hint: {'x': .1, 'y': .55}  
            normal_color: app.theme_cls.accent_light
            foreground_color : app.theme_cls.text_color
            # pos_hint: {'center_x': .5}
            on_text: root.get_subcategory()
            helper_text_mode: 'on_focus'  
            helper_text: 'Enter a new sub-category'  
            max_text_length: 20
            input_filter: root.text_filter            
        MDFillRoundFlatButton:
            id: submit
            size_hint_x : .75
            pos_hint: {'x': .1, 'y': .4}  
            text: 'Submit'
            elevation: 10
            #disabled : True
            on_release: root.on_submit() 
        MDLabel:
            id: lbl_message    
            size_hint : (.8, .1)
            pos_hint: {'x': .1, 'y': .25}                 
            halign: 'center' 
            theme_text_color: "Primary" 
'''


class CustomFlatButton(MDRectangleFlatButton):
    def __init__(self, **kwargs):
        super(CustomFlatButton, self).__init__(**kwargs)
        self.md_bg_color = kwargs['md_bg_color']
        self.increment_width = kwargs['width'] - len(self.text)


class AddItem(Screen):
    """Class for adding a new item"""
    cat_dropdown = DropDown()
    subcat_dropdown = DropDown()

    def __init__(self, **kwargs):
        self.name = 'AddItem'
        global app_scr
        app_scr = kwargs['app']
        super(AddItem, self).__init__()
        self.cat_dropdown.bind(on_select=lambda instance, x: setattr(self.ids.category, 'text', x))
        self.subcat_dropdown.bind(on_select=lambda instance, x: setattr(self.ids.subcategory, 'text', x))

    def get_category(self, *args):
        """function to get MAIN items based on the search text entered by user"""
        if app_scr.item_type == 'main':
            return  # we dont need to display dropdown when creating new main item.

        self.cat_dropdown.clear_widgets()
        if self.cat_dropdown.attach_to is not None:
            self.cat_dropdown._real_dismiss()
        item_name = self.ids.category.text
        item_dict = {}
        if item_name is not None and item_name != '' and args[0] != 'button':
            item_dict = Items.get_items(item_name=item_name, item_type='main')
        if args[0] == 'button':
            item_dict = Items.get_items(item_name='', item_type='main')
        if item_dict != {}:
            for key, value in item_dict.items():
                self.cat_dropdown.add_widget(CustomFlatButton(text=value['item_name'],
                                                              on_release=lambda x:
                                                              self.cat_dropdown.select(x.text),
                                                              md_bg_color=app_scr.theme_cls.accent_light,
                                                              width=self.ids.category.width))
            self.cat_dropdown.open(self.ids.category)

    def get_subcategory(self):
        """function to get SUB items based on the search text entered by user"""

        self.subcat_dropdown.clear_widgets()
        if self.subcat_dropdown.attach_to is not None:
            self.subcat_dropdown._real_dismiss()
        item_name = self.ids.subcategory.text
        if item_name is not None and item_name != '':
            item_dict = Items.get_items(item_name=item_name, item_type='sub')
            for key, value in item_dict.items():
                self.subcat_dropdown.add_widget(CustomFlatButton(text=value['item_name'],
                                                                 on_release=lambda x:
                                                                 self.subcat_dropdown.select(x.text),
                                                                 md_bg_color=app_scr.theme_cls.accent_light,
                                                                 width=self.ids.subcategory.width))
            self.subcat_dropdown.open(self.ids.subcategory)

    def on_submit(self):
        if self.ids.category.text is None or self.ids.category.text == '':  # category not empty
            self.ids.lbl_message.text = 'Required inputs missing'
            self.ids.lbl_message.theme_text_color = 'Error'
            return

        cat_item_id = Items.get_item(item_name=self.ids.category.text, item_link=0)
        if cat_item_id is not None:  # category exists
            if self.ids.subcategory.text is not None and self.ids.subcategory.text != '':
                sub_cat_item_id = Items.get_item(item_name=self.ids.subcategory.text, item_link=cat_item_id)
                if sub_cat_item_id is not None:
                    self.ids.lbl_message.text = 'Sub-Category already exists'
                    self.ids.lbl_message.theme_text_color = 'Error'
                else:
                    params = {'item_id': Items.get_next_item_id(),
                              'item_name': self.ids.subcategory.text,
                              'active': True,
                              'item_link': cat_item_id}
                    Items.add_item(**params)
                    toast('Sub-Category created')
                    app_scr.screens.item_refresh_rqd = True
                    self.leave_screen()
            else:
                if app_scr.item_type != 'main':
                    self.ids.lbl_message.text = 'Required inputs missing'
                    self.ids.lbl_message.theme_text_color = 'Error'
                else:
                    self.ids.lbl_message.text = 'Category already exists'
                    self.ids.lbl_message.theme_text_color = 'Error'

        else:  # category doesn't exist
            if app_scr.item_type != 'main':
                self.ids.lbl_message.text = 'Category doesn\'t exist'
                self.ids.lbl_message.theme_text_color = 'Error'
            else:
                params = {'item_id': Items.get_next_item_id(),
                          'item_name': self.ids.category.text,
                          'active': True,
                          'item_link': 0}
                Items.add_item(**params)
                toast('Categoty created')
                app_scr.screens.item_refresh_rqd = True
                self.leave_screen()

    def leave_screen(self, *args):
        app_scr.screens.show_screen('Items')

    def on_pre_enter(self, *args):
        self.ids.category.text = ''
        self.ids.subcategory.text = ''
        self.ids.lbl_message.text = ''
        # self.ids.active.active = False
        if app_scr.item_type == 'main':
            self.ids.lbl_item_type.text = 'New Category'
            self.ids.subcategory.disabled = True
            self.ids.category.helper_text = 'Enter a new category'
        else:
            self.ids.lbl_item_type.text = 'New Sub-Category'
            self.ids.subcategory.disabled = False
            self.ids.category.helper_text = 'Type/Select from dropdown'

    def on_enter(self, *args):
        self.ids.category.focus = True
        if app_scr.item_type == 'main':
            self.ids.drop_button.disabled = True
        else:
            self.ids.drop_button.disabled = False

    def text_filter(self, input_text, undo_flag):
        if input_text.isalnum():
            return input_text
        else:
            return

    def on_leave(self, *args):
        self.cat_dropdown.clear_widgets()
        self.subcat_dropdown.clear_widgets()


