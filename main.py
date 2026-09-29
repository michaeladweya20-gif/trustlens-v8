from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

class Page1(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        b=BoxLayout(orientation='vertical',padding=15,spacing=10)
        b.add_widget(Label(text='1 - Email / Password',size_hint=(1,0.1)))
        b.add_widget(TextInput(hint_text='Email',text='labourf65@gmail.com',multiline=False,size_hint=(1,0.12)))
        b.add_widget(TextInput(hint_text='Password',password=True,multiline=False,size_hint=(1,0.12)))
        r=BoxLayout(spacing=10,size_hint=(1,0.15))
        r.add_widget(Button(text='Sign in'))
        go=Button(text='log In',background_color=(0.75,0.15,0.18,1))
        go.bind(on_press=lambda x: setattr(self.manager,'current','ent'))
        r.add_widget(go)
        b.add_widget(r)
        self.add_widget(b)

class Page2(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        b=BoxLayout(orientation='vertical',padding=15,spacing=8)
        b.add_widget(Label(text='2 Ent. - Inbox handling all handle',size_hint=(1,0.1)))
        b.add_widget(TextInput(hint_text='search - break bulky opportunities',multiline=False,size_hint=(1,0.1)))
        b.add_widget(TextInput(hint_text='Account Name',multiline=False,size_hint=(1,0.1)))
        b.add_widget(TextInput(hint_text='Password - encrypted locally',password=True,multiline=False,size_hint=(1,0.1)))
        b.add_widget(Label(text='Checking YOUR apps: Gmail, X, WhatsApp',font_size='12sp',size_hint=(1,0.3)))
        nav=BoxLayout(spacing=5,size_hint=(1,0.12))
        nav.add_widget(Button(text='Back',on_press=lambda x: setattr(self.manager,'current','login')))
        nav.add_widget(Button(text='Next ->',on_press=lambda x: setattr(self.manager,'current','cat')))
        b.add_widget(nav)
        self.add_widget(b)

class Page3(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        b=BoxLayout(orientation='vertical',padding=15,spacing=12)
        b.add_widget(Label(text='3 - sports / charity / organization',size_hint=(1,0.1)))
        b.add_widget(TextInput(hint_text='search opportunities',multiline=False,size_hint=(1,0.1)))
        for n in ['sports','charity','organization']:
            btn=Button(text=n,size_hint=(1,0.18))
            if n=='sports': btn.bind(on_press=lambda x: setattr(self.manager,'current','sports'))
            b.add_widget(btn)
        self.add_widget(b)

class Page4(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        b=BoxLayout(orientation='vertical',padding=15,spacing=5)
        b.add_widget(Label(text='4 Sports - who where how',size_hint=(1,0.08)))
        b.add_widget(TextInput(hint_text='- who',multiline=False,size_hint=(1,0.1)))
        b.add_widget(TextInput(hint_text='- where Eldoret/Kisumu/Nairobi',multiline=False,size_hint=(1,0.1)))
        b.add_widget(TextInput(hint_text='- how Jobs/Trials',multiline=False,size_hint=(1,0.1)))
        b.add_widget(TextInput(hint_text='- which social',multiline=False,size_hint=(1,0.1)))
        b.add_widget(TextInput(hint_text='- media handle @athletics_kenya',multiline=False,size_hint=(1,0.1)))
        b.add_widget(TextInput(hint_text='-> Search',multiline=False,size_hint=(1,0.1)))
        b.add_widget(Button(text='Back',size_hint=(1,0.1),on_press=lambda x: setattr(self.manager,'current','cat')))
        self.add_widget(b)

class Page5(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        b=BoxLayout(orientation='vertical',padding=15)
        b.add_widget(Label(text='5 Microsoft Off.cc 5525\nFishing rods: diversification, specialization, location, culture'))
        b.add_widget(Button(text='Go to Start',on_press=lambda x: setattr(self.manager,'current','login')))
        self.add_widget(b)

class TrustLensApp(App):
    def build(self):
        sm=ScreenManager()
        sm.add_widget(Page1(name='login'))
        sm.add_widget(Page2(name='ent'))
        sm.add_widget(Page3(name='cat'))
        sm.add_widget(Page4(name='sports'))
        sm.add_widget(Page5(name='microsoft'))
        return sm
TrustLensApp().run()
