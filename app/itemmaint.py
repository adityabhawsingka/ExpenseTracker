from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App

from dtclasses import Items
from stackfloatingbuttons import MDStackFloatingButtons

itemsmaint = '''
#:import MDTextFieldRound kivymd.textfields.MDTextFieldRound
#:import MDCheckbox kivymd.selectioncontrols.MDCheckbox
#:import MDLabel kivymd.label.MDLabel

<ItemsMaint>

    BoxLayout:
        orientation: 'vertical'
        spacing : 5
        padding: 5

        MDTextFieldRound:
            id: search
            icon_left: 'feature-search'
            icon_type: 'left'
            normal_color: app.theme_cls.divider_color
            pos_hint: {'center_x': .5}
            size_hint_x: .9
            # width: 250
            hint_text: 'Search Item'
            foreground_color: app.theme_cls.text_color
            elevation: 10
            on_text: root.search()
        ScrollView:
            id: itemscroll
            do_scroll_x: False
            RecycleView:
                id: rv_items
                viewclass: 'ListItem'
                RecycleBoxLayout: 
                    default_size: None, dp(45)
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: 'vertical'             
        BoxLayout:
            id: box_button
            orientation: 'vertical'
            size_hint_y: 0.005

<ListItem>:
    canvas.before:
        Color:
            rgba: app.theme_cls.primary_light if root.item_link == 0 else app.theme_cls.bg_normal
        Rectangle:
            size: (self.width, self.height)
            pos: self.pos
        Color:
            rgba: app.theme_cls.divider_color
        Line:
            width: .5
            points: [self.x, self.y, self.x + self.width, self.y ]                
    MDLabel:
        id: itemname
        pos_hint: {'x': 0.05 ,'y':0}
        size_hint_x: .55
        theme_text_color: "Primary" if root.item_link == 0 else "Secondary"
        markup: True
    MDCheckbox:
        id: active_box
        pos_hint: {'x': .6 ,'y':0}
        size_hint_x: .4
        active: root.rv_key in app.item_selection
        on_active:
            root.on_active(app)
'''

itemsmaint_obj = ObjectProperty()


class ListItem(FloatLayout):
    """Class to create a list item on the item maintenance screen"""
    data = ObjectProperty()
    item_id = NumericProperty()
    item_link = NumericProperty()
    rv_key = NumericProperty(0)

    def __init__(self, **kwargs):
        super(ListItem, self).__init__(**kwargs)

    def on_active(self, *args):
        app = args[0]
        active = self.ids.active_box.active
        if active and self.rv_key not in app.item_selection:
            result = Items.update_active(item_id=self.item_id, active=self.ids.active_box.active)
            if result == 'revert':
                self.ids.active_box.active = False
            else:
                itemsmaint_obj.refresh_list()
        elif not active and self.rv_key in app.item_selection:
            result = Items.update_active(item_id=self.item_id, active=self.ids.active_box.active)
            itemsmaint_obj.refresh_list()

    def on_data(self, *args):
        self.ids.itemname.text = self.data["text"]
        self.item_id = self.data["item_id"]
        self.item_link = self.data["item_link"]


class ItemsMaint(Screen):
    """Main class for item maintenance screen"""

    app = App.get_running_app()
    refresh_in_progress = False

    def __init__(self, **kwargs):
        self.name = 'Items'
        super(ItemsMaint, self).__init__()
        global app_scr, itemsmaint_obj
        app_scr = kwargs['app']
        itemsmaint_obj = self
        self.ids.box_button.add_widget(MDStackFloatingButtons(icon='plus',
                                                              floating_data={'Category': 'alpha-c',
                                                                             'Sub-Category': 'alpha-s'
                                                                             },
                                                              callback=self.add_item
                                                              )
                                       )

    def refresh_list(self):
        """Function to populate list of items"""
        self.refresh_in_progress = True
        self.ids.search.text = ''

        self.app.item_selection = {}
        recycle_data = []
        item_dict = Items.get_main_items()  # fetch all main items
        rv_key = 0
        # Loop on the fetched main items
        for item_id, item in item_dict.items():
            # Get sub-items linked to the main item
            subitems = Items.get_items_by_link(item_link=item_id)
            i_dict = {"data": {"item_id": item_id,
                               "active": item['active'],
                               "item_link": 0,
                               "text": item['item_name'],
                               "theme_text_color": 'Primary'},
                      "rv_key": rv_key}
            if item['active'] is True:
                self.app.item_selection[rv_key] = [rv_key]
            rv_key += 1

            recycle_data.append(i_dict)

            # Loop on sub-items and add them to the Boxlayout
            for sub_id, sub_item in subitems.items():
                i_dict = {"data": {"text": f"    {sub_item['item_name']}",
                                    "item_id": sub_id,
                                    "active": sub_item['active'],
                                    "item_link": item_id,
                                    "theme_text_color": 'Secondary'},
                          "rv_key": rv_key}

                if sub_item['active'] is True:
                    self.app.item_selection[rv_key] = [rv_key]

                rv_key += 1

                recycle_data.append(i_dict)

        self.ids.rv_items.data = recycle_data
        self.refresh_in_progress = False

    def add_item(self, instance):
        if instance.icon == 'alpha-c':
            app_scr.item_type = 'main'
        else:
            app_scr.item_type = 'sub'
        app_scr.screens.show_screen('AddItem')

    def search(self):
        if self.refresh_in_progress is True:
            return
        search_text = self.ids.search.text
        if search_text == '':
            self.refresh_list()
        else:
            self.app.item_selection = {}
            recycle_data = []
            item_dict = Items.get_items(item_type='all', item_name=search_text)
            rv_key = 0
            for item_id, item in item_dict.items():
                if item['item_link'] == 0:
                    subtext = 'Category'
                else:
                    subtext = 'Sub-Category'
                i_dict = {"data": {"item_id": item_id,
                                   "active": item['active'],
                                   "item_link": -1,
                                   "text": '{}    [color=#999][size=18][i]{}[/i][/size][/color]'.format(item['item_name'], subtext),
                                   "theme_text_color": 'Secondary'},
                          "rv_key": rv_key}
                if item['active'] is True:
                    self.app.item_selection[rv_key] = [rv_key]
                rv_key += 1
                recycle_data.append(i_dict)
            self.ids.rv_items.data = recycle_data

    def on_pre_enter(self):
        self.ids.search.text = ''

    def on_enter(self, *args):
         if app_scr.screens.item_refresh_rqd is True:
            self.refresh_list()
            app_scr.screens.item_refresh_rqd = False
