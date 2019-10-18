from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

kv = '''
#:import MDToolbar kivymd.toolbar.MDToolbar
#:import MDLabel kivymd.label.MDLabel
#:import MDSeparator kivymd.cards.MDSeparator
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout
#:import NavigationDrawerToolbar kivymd.navigationdrawer.NavigationDrawerToolbar
#:import NavigationDrawerSubheader kivymd.navigationdrawer.NavigationDrawerSubheader

<NavDrawerIconButton@NavigationDrawerIconButton>
    on_release:
        app.screens.show_screen(root.text)

<ContentNavigationDrawer@MDNavigationDrawer>
    drawer_logo: './data/images/icon.png'
    use_logo: 'logo'
    elevation: 10
        
    NavDrawerIconButton:
        icon : 'view-dashboard'
        text: "Dashboard"

    NavDrawerIconButton:
        icon : 'wallet'
        text: "Expenses"         

    NavDrawerIconButton:
        icon : 'star-four-points'
        text: "Items" 

    NavDrawerIconButton:
        icon : 'eye-outline'
        text: "Insights"                        

    NavDrawerIconButton:
        icon : 'settings'
        text: "Settings"   

<NavigationScreen@Screen>
    name: 'NavigationScreen'
    nav_layout : nav_layout
    opacity: 0
    on_enter:
        app.screens.show_screen('Dashboard')
        root.opacity=  1
    NavigationLayout:
        id: nav_layout
        nav_drawer : nav_drawer.__self__
        toolbar : toolbar.__self__
        scrn_mgr : scrn_mgr.__self__
        
        ContentNavigationDrawer:
            id: nav_drawer          
      
        BoxLayout:
            orientation: 'vertical'      
            MDToolbar:
                id: toolbar
                title: app.title
                md_bg_color: app.theme_cls.primary_color
                background_palette: 'Primary'
                background_hue: '500'
                elevation: 10    
                left_action_items:
                    [['menu', lambda x: nav_layout.toggle_nav_drawer()]]
                right_action_items:
                    [['dots-vertical', lambda x: nav_layout.toggle_nav_drawer()]]

            ScreenManager:
                id: scrn_mgr 

            Widget:
                size_hint: (None, None)
                size: (0, 0)

'''


class NavigationScreen(Screen):
    Builder.load_string(kv)

    def __init__(self):
        super(NavigationScreen, self).__init__()
        from kivy.app import App
        import os.path
        import shutil
        from dtclasses import init_session
        app = App.get_running_app()
        f_path = app.user_data_dir
        f_path = os.path.join(f_path, 'extrac.db')
        if os.path.isfile(f_path) is False:
            shutil.copyfile('./extrac.db', f_path)
        init_session(f_path)