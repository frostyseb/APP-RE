from kivy.uix.screenmanager import ScreenManager, Screen

sm = ScreenManager()
sm.add_widget(Screen(name='main'))
sm.add_widget(Screen(name='result'))
sm.add_widget(Screen(name='app'))
