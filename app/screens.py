from kivy.factory import Factory
from kivy.lang import Builder


class Screens(object):
    primary_widget = None
    current_tab = 'day'
    item_refresh_rqd = True
    item_type = 'main'
    app = ""
    current_screen = 'None'

    data = {
        'Dashboard':
            {'kv_string': "",
             'Factory': 'Factory.Dashboard(app=self.app)',
             'name_screen': 'Dashboard',
             'object': None},

        'Expenses':
            {'kv_string': "",
             'Factory': 'Factory.Dashboard2(app=self.app)',
             'name_screen': 'Dashboard2',
             'object': None},

        'Add Expense':
            {'kv_string': "",
             'Factory': 'Factory.AddExpense(app=self.app)',
             'name_screen': 'Add Expense',
             'object': None},

        'Items':
            {'kv_string': "",
             'Factory': 'Factory.ItemsMaint(app=self.app)',
             'name_screen': 'Items',
             'object': None},

        'Insights':
            {'kv_string': "",
             'Factory': 'Factory.Insights(app=self.app)',
             'name_screen': 'Insights',
             'object': None},

        'Settings':
            {'kv_string': "",
             'Factory': 'Factory.SettingsPage(app=self.app)',
             'name_screen': 'Settings',
             'object': None},

        'AddItem':
            {'kv_string': "",
             'Factory': 'Factory.AddItem(app=self.app)',
             'name_screen': 'AddItem',
             'object': None}


    }

    def show_screen(self, name_screen, **kwargs):
        if self.current_screen == name_screen:
            return
        if not self.data[name_screen]['object']:
            if name_screen == 'Dashboard':
                from dashboard import Dashboard, dashboard
                self.data[name_screen]['kv_string'] = dashboard
            elif name_screen == 'Insights':
                from insights import insights_kv, Insights
                self.data[name_screen]['kv_string'] = insights_kv
            elif name_screen == 'Items':
                from itemmaint import itemsmaint, ItemsMaint
                self.data[name_screen]['kv_string'] = itemsmaint
            elif name_screen == 'Settings':
                from settings import settings_kv, SettingsPage
                self.data[name_screen]['kv_string'] = settings_kv
            elif name_screen == 'AddItem':
                from additem import additem, AddItem
                self.data[name_screen]['kv_string'] = additem
            elif name_screen == 'Add Expense':
                from addexpense import add_expense, AddExpense
                self.data[name_screen]['kv_string'] = add_expense
            elif name_screen == 'Expenses':
                from expdetail import dashboard2, Dashboard2
                self.data[name_screen]['kv_string'] = dashboard2

            Builder.load_string(self.data[name_screen]['kv_string'])
            self.data[name_screen]['object'] = eval(self.data[name_screen]['Factory'])
            self.primary_widget.ids.scrn_mgr.add_widget(self.data[name_screen]['object'])

        self.primary_widget.ids.scrn_mgr.current = self.data[name_screen]['name_screen']
        self.current_screen = name_screen




