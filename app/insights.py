from kivy.uix.screenmanager import Screen
from kivymd.label import MDLabel
from kivymd.cards import MDCard
from dtclasses import Expenses
from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from kivymd.accordion import MDAccordionItem2
from kivy.uix.floatlayout import FloatLayout

insights_kv = '''
<Insights>
    # on_enter: app.set_accordion_list()
    # on_leave: anim_list.clear_widgets()set_accordion_list
    insight_list : insight_list.__self__
    ScrollView:
        Accordion:
            id: insight_list
            orientation: 'vertical'
            padding : '12dp'
            spacing : '12dp'
'''


class Insights(Screen):
    def __init__(self, **kwargs):
        self.name = 'Insights'
        global app_scr
        app_scr = kwargs['app']
        super(Insights, self).__init__()

    def cre_list(self):
        self.ids.insight_list.clear_widgets()
        # Get maximum and minimum info.
        currency = app_scr.config.get('CustSettings', 'Currency')

        layout_box = FloatLayout()
        card_ = MDCard(orientation='vertical', border_radius=10, border_color_a=0.2,
                       elevation=10, size_hint=(.95, .95), pos_hint={'x': .025, 'y': .025})
        layout_box.add_widget(card_)

        max_dict = Expenses.get_borders()

        # Get the most expensive day.
        disp_data = max_dict['MEDay']
        card_.add_widget(MDLabel(text='Most Expensive Day',
                                 halign='center',
                                 bold=True,
                                 font_style='Subtitle1',
                                 theme_text_color='Primary'
                                 ))
        box_meday = BoxLayout()
        box_meday.add_widget(
            MDLabel(text='    {}'.format(datetime.strptime(disp_data['date'], '%Y-%m-%d').strftime('%d %b %Y'))
                    , halign='center'
                    , theme_text_color='Primary'
                    , size_hint_x=.5))
        box_meday.add_widget(MDLabel(text='{} {}'.format(currency, disp_data['value'])
                                     , halign='center'
                                     , theme_text_color='Primary'
                                     , size_hint_x=.5))
        card_.add_widget(box_meday)

        # Get the least expensive day.
        disp_data = max_dict['LEDay']
        card_.add_widget(MDLabel(text='Least Expensive Day',
                                 halign='center',
                                 bold=True,
                                 font_style='Subtitle1',
                                 theme_text_color='Primary'
                                 ))
        box_leday = BoxLayout()
        box_leday.add_widget(
            MDLabel(text='    {}'.format(datetime.strptime(disp_data['date'], '%Y-%m-%d').strftime('%d %b %Y'))
                    , halign='center'
                    , theme_text_color='Primary'
                    , size_hint_x=.5))
        box_leday.add_widget(MDLabel(text='{} {}'.format(currency, disp_data['value'])
                                     , halign='center'
                                     , theme_text_color='Primary'
                                     , size_hint_x=.5))
        card_.add_widget(box_leday)

        # Get the most expensive month.
        disp_data = max_dict['MEMonth']
        card_.add_widget(MDLabel(text='Most Expensive Month',
                                 halign='center',
                                 bold=True,
                                 font_style='Subtitle1',
                                 theme_text_color='Primary'
                                 ))
        box_memonth = BoxLayout()
        box_memonth.add_widget(
            MDLabel(text='    {}'.format(datetime.strptime(disp_data['date'], '%Y-%m').strftime('%b %Y'))
                    , halign='center'
                    , theme_text_color='Primary'
                    , size_hint_x=.5))
        box_memonth.add_widget(MDLabel(text='{} {}'.format(currency, disp_data['value'])
                                       , halign='center'
                                       , theme_text_color='Primary'
                                       , size_hint_x=.5))
        card_.add_widget(box_memonth)

        # Get the least expensive month.
        disp_data = max_dict['LEMonth']
        card_.add_widget(MDLabel(text='Least Expensive Month',
                                 halign='center',
                                 bold=True,
                                 font_style='Subtitle1',
                                 theme_text_color='Primary'
                                 ))
        box_lemonth = BoxLayout()
        box_lemonth.add_widget(
            MDLabel(text='    {}'.format(datetime.strptime(disp_data['date'], '%Y-%m').strftime('%b %Y'))
                    , halign='center'
                    , theme_text_color='Primary'
                    , size_hint_x=.5))
        box_lemonth.add_widget(MDLabel(text='{} {}'.format(currency, disp_data['value'])
                                       , halign='center'
                                       , theme_text_color='Primary'
                                       , size_hint_x=.5))
        card_.add_widget(box_lemonth)

        card_.add_widget(BoxLayout())
        # Add the box to accorion list item
        acc_im = MDAccordionItem2(title='Max-Mins')
        acc_im.add_widget(layout_box)
        self.ids.insight_list.add_widget(acc_im)

        # Averages
        layout_boxa = FloatLayout()
        card_a = MDCard(orientation='vertical', border_radius=10, border_color_a=0.2,
                        elevation=10, size_hint=(.95, .5), pos_hint={'x': .025, 'y': .475})
        layout_boxa.add_widget(card_a)

        avg_dict = Expenses.get_avgs()

        # Get the average daily expense.
        disp_data = avg_dict['day_avg']
        box_avgday = BoxLayout()
        box_avgday.add_widget(
            MDLabel(text='    {}'.format('Average Daily Expense')
                    , halign='center'
                    , bold=True
                    , theme_text_color='Primary'
                    , size_hint_x=.5))
        box_avgday.add_widget(MDLabel(text='{} {}'.format(currency, disp_data)
                                      , halign='center'
                                      , theme_text_color='Primary'
                                      , size_hint_x=.5))
        card_a.add_widget(box_avgday)

        # Get the average monthly expense.
        disp_data = avg_dict['month_avg']
        box_avgmonth = BoxLayout()
        box_avgmonth.add_widget(
            MDLabel(text='    {}'.format('Average Monthly Expense')
                    , halign='center'
                    , bold=True
                    , theme_text_color='Primary'
                    , size_hint_x=.5))
        box_avgmonth.add_widget(MDLabel(text='{} {}'.format(currency, disp_data)
                                        , halign='center'
                                        , theme_text_color='Primary'
                                        , size_hint_x=.5))
        card_a.add_widget(box_avgmonth)

        # Get the average daily expense.
        disp_data = avg_dict['year_avg']
        box_avgyear = BoxLayout()
        box_avgyear.add_widget(
            MDLabel(text='    {}'.format('Average Yearly Expense')
                    , halign='center'
                    , bold=True
                    , theme_text_color='Primary'
                    , size_hint_x=.5))
        box_avgyear.add_widget(MDLabel(text='{} {}'.format(currency, disp_data)
                                       , halign='center'
                                       , theme_text_color='Primary'
                                       , size_hint_x=.5))
        card_a.add_widget(box_avgyear)

        acc_ia = MDAccordionItem2(title='Averages')
        acc_ia.add_widget(layout_boxa)
        self.ids.insight_list.add_widget(acc_ia)

    def on_leave(self, *args):
        self.ids.insight_list.clear_widgets()

    def on_enter(self):
        self.cre_list()