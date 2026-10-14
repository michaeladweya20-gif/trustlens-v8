import hashlib
import json
import os
import secrets
import webbrowser
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.utils import get_color_from_hex


BG = "#101827"
PANEL = "#1B2738"
ACCENT = "#42D6B3"
TEXT = "#F4F7FB"
MUTED = "#AAB7C8"
DATA = [
    {"title": "Kenya sports opportunities", "category": "Sports", "detail": "Trials, athlete development and sports updates.", "url": "https://www.sportskenya.org/"},
    {"title": "Athletics Kenya", "category": "Sports", "detail": "Federation updates, events and athletics information.", "url": "https://athleticskenya.or.ke/"},
    {"title": "BrighterMonday Kenya", "category": "Jobs", "detail": "Search jobs and career opportunities in Kenya.", "url": "https://www.brightermonday.co.ke/"},
    {"title": "Fuzu Kenya", "category": "Jobs", "detail": "Jobs, career guidance and professional development.", "url": "https://www.fuzu.com/kenya"},
    {"title": "Kenya Red Cross", "category": "Volunteering", "detail": "Humanitarian programmes and ways to get involved.", "url": "https://www.redcross.or.ke/"},
    {"title": "Volunteer opportunities", "category": "Volunteering", "detail": "Explore volunteer placements and community projects.", "url": "https://www.volunteerworld.com/"},
    {"title": "Kenya National Chamber of Commerce", "category": "Organizations", "detail": "Business networking, events and organization information.", "url": "https://kenyachamber.or.ke/"},
    {"title": "Public Service Commission Kenya", "category": "Jobs", "detail": "Public service vacancies and official announcements.", "url": "https://www.publicservice.go.ke/"},
]


def colors(hex_value):
    return get_color_from_hex(hex_value)


def make_label(text, size=15, color=TEXT, height=None, bold=False):
    widget = Label(text=text, color=colors(color), font_size=sp(size),
                   bold=bold, halign="left", valign="middle",
                   size_hint_y=None if height else 1, height=dp(height) if height else None)
    widget.bind(size=lambda instance, value: setattr(instance, "text_size", (value[0], None)))
    return widget


def sp(value):
    return dp(value)


class BaseScreen(Screen):
    def page(self, heading, subtitle=""):
        root = BoxLayout(orientation="vertical", padding=dp(18), spacing=dp(12))
        root.add_widget(make_label("TRUSTLENS", 13, ACCENT, 24, True))
        root.add_widget(make_label(heading, 25, TEXT, 38, True))
        if subtitle:
            root.add_widget(make_label(subtitle, 13, MUTED, 42))
        self.body = BoxLayout(orientation="vertical", spacing=dp(10))
        root.add_widget(self.body)
        self.add_widget(root)
        return root

    def button(self, title, callback, color=ACCENT, text_color=BG, height=46):
        btn = Button(text=title, size_hint_y=None, height=dp(height),
                     background_normal="", background_color=colors(color),
                     color=colors(text_color), bold=True, font_size=dp(14))
        btn.bind(on_release=callback)
        return btn

    def field(self, hint, password=False):
        return TextInput(hint_text=hint, password=password, multiline=False,
                         size_hint_y=None, height=dp(48), padding=(dp(12), dp(13)),
                         background_normal="", background_active="",
                         background_color=colors(PANEL), foreground_color=colors(TEXT),
                         hint_text_color=colors(MUTED), cursor_color=colors(ACCENT))


class LoginScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page("Opportunity starts here", "Find jobs, sports pathways and ways to serve your community.")
        self.body.add_widget(make_label("Sign in or create a local account", 16, TEXT, 30, True))
        self.email = self.field("Email address")
        self.password = self.field("Password (at least 8 characters)", True)
        self.body.add_widget(self.email)
        self.body.add_widget(self.password)
        self.message = make_label("", 13, ACCENT, 44)
        self.body.add_widget(self.message)
        self.body.add_widget(self.button("Sign in", self.sign_in))
        self.body.add_widget(self.button("Create account", self.sign_up, PANEL, TEXT))
        self.body.add_widget(make_label("Your account is stored on this device. Use a unique password. No password is sent to TrustLens.", 12, MUTED, 60))

    def sign_in(self, *_):
        email = self.email.text.strip().lower()
        password = self.password.text
        user = App.get_running_app().users.get(email)
        if user and verify_password(password, user):
            app = App.get_running_app()
            app.current_email = email
            app.open_home()
        else:
            self.message.text = "Email or password is incorrect."

    def sign_up(self, *_):
        email = self.email.text.strip().lower()
        password = self.password.text
        app = App.get_running_app()
        if "@" not in email or "." not in email.split("@")[-1]:
            self.message.text = "Enter a valid email address."
            return
        if len(password) < 8:
            self.message.text = "Choose a password with at least 8 characters."
            return
        if email in app.users:
            self.message.text = "Account exists. Please sign in."
            return
        app.users[email] = hash_password(password)
        app.save_users()
        app.current_email = email
        app.add_notice("Welcome to TrustLens", "Your local account is ready. Explore opportunities and save the ones you like.")
        app.open_home()


class HomeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page("Your next step, clearer.", "Search opportunities from trusted public sources.")
        self.body.add_widget(make_label("Explore by interest", 16, TEXT, 28, True))
        for name, screen in [("Find opportunities", "opportunities"), ("Saved opportunities", "saved"), ("Updates inbox", "notifications"), ("Connections & integrations", "integrations")]:
            self.body.add_widget(self.button(name, lambda _btn, target=screen: setattr(self.manager, "current", target), PANEL, TEXT))
        self.body.add_widget(make_label("TrustLens opens public provider websites. It does not claim to be affiliated with them.", 12, MUTED, 54))
        self.body.add_widget(self.button("Sign out", self.sign_out, "#344258", TEXT))

    def sign_out(self, *_):
        App.get_running_app().current_email = ""
        self.manager.current = "login"


class OpportunitiesScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page("Discover opportunities", "Filter the starter directory, then open the provider for full details.")
        self.search = self.field("Search by title, place or keyword")
        self.search.bind(text=lambda *_: self.render_results())
        self.body.add_widget(self.search)
        row = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(6))
        for category in ["All", "Jobs", "Sports", "Volunteering", "Organizations"]:
            row.add_widget(self.button(category, lambda _b, c=category: self.set_category(c), PANEL, TEXT, 42))
        self.body.add_widget(row)
        self.results = GridLayout(cols=1, spacing=dp(8), size_hint_y=None)
        self.results.bind(minimum_height=self.results.setter("height"))
        scroll = ScrollView()
        scroll.add_widget(self.results)
        self.body.add_widget(scroll)
        self.active_category = "All"
        self.body.add_widget(self.button("Back to home", lambda *_: setattr(self.manager, "current", "home"), "#344258", TEXT))
        self.render_results()

    def set_category(self, category):
        self.active_category = category
        self.render_results()

    def render_results(self):
        if not hasattr(self, "results"):
            return
        self.results.clear_widgets()
        query = self.search.text.strip().lower()
        app = App.get_running_app()
        for item in DATA:
            haystack = " ".join([item["title"], item["category"], item["detail"]]).lower()
            if self.active_category not in ("All", item["category"]) or query not in haystack:
                continue
            card = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(5),
                             size_hint_y=None, height=dp(142))
            card.add_widget(make_label(item["title"], 15, ACCENT, 26, True))
            card.add_widget(make_label(item["category"] + " · " + item["detail"], 12, MUTED, 42))
            actions = BoxLayout(size_hint_y=None, height=dp(38), spacing=dp(8))
            actions.add_widget(self.button("Open website", lambda _b, url=item["url"]: open_url(url), ACCENT, BG, 38))
            actions.add_widget(self.button("Save", lambda _b, data=item: app.save_opportunity(data), PANEL, TEXT, 38))
            card.add_widget(actions)
            card.canvas.before.clear()
            self.results.add_widget(card)
        if not self.results.children:
            self.results.add_widget(make_label("No matches. Try another keyword or category.", 13, MUTED, 48))


class SavedScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page("Saved opportunities", "Your saved list is stored locally on this device.")
        self.listing = GridLayout(cols=1, spacing=dp(8), size_hint_y=None)
        self.listing.bind(minimum_height=self.listing.setter("height"))
        scroll = ScrollView()
        scroll.add_widget(self.listing)
        self.body.add_widget(scroll)
        self.body.add_widget(self.button("Back to home", lambda *_: setattr(self.manager, "current", "home"), "#344258", TEXT))
        self.bind(on_pre_enter=lambda *_: self.refresh())

    def refresh(self):
        self.listing.clear_widgets()
        app = App.get_running_app()
        saved = app.saved.get(app.current_email, [])
        if not saved:
            self.listing.add_widget(make_label("Nothing saved yet. Visit Discover opportunities to save items.", 13, MUTED, 55))
        for item in saved:
            self.listing.add_widget(make_label(item["title"] + " · " + item["category"], 14, TEXT, 34, True))
            self.listing.add_widget(self.button("Open provider", lambda _b, url=item["url"]: open_url(url), PANEL, TEXT, 38))


class IntegrationsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page("Connections", "Open official services. Secure sign-in and account linking are not implemented yet.")
        self.body.add_widget(make_label("For your safety, never enter Gmail, X or WhatsApp passwords into TrustLens.", 13, MUTED, 60))
        self.body.add_widget(self.button("Open Gmail", lambda *_: open_url("https://mail.google.com/"), PANEL, TEXT))
        self.body.add_widget(self.button("Open X", lambda *_: open_url("https://x.com/"), PANEL, TEXT))
        self.body.add_widget(self.button("Open WhatsApp Web", lambda *_: open_url("https://web.whatsapp.com/"), PANEL, TEXT))
        self.body.add_widget(make_label("These buttons open the provider website; they do not connect, read, or sync your accounts.", 12, MUTED, 55))
        self.body.add_widget(self.button("Back to home", lambda *_: setattr(self.manager, "current", "home"), "#344258", TEXT))


class NotificationsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page("Updates inbox", "Local notices and reminders from inside TrustLens.")
        self.items = GridLayout(cols=1, spacing=dp(8), size_hint_y=None)
        self.items.bind(minimum_height=self.items.setter("height"))
        scroll = ScrollView()
        scroll.add_widget(self.items)
        self.body.add_widget(scroll)
        self.body.add_widget(self.button("Back to home", lambda *_: setattr(self.manager, "current", "home"), "#344258", TEXT))
        self.bind(on_pre_enter=lambda *_: self.refresh())

    def refresh(self):
        self.items.clear_widgets()
        notices = App.get_running_app().notices
        if not notices:
            self.items.add_widget(make_label("You're all caught up.", 14, MUTED, 42))
        for item in reversed(notices):
            self.items.add_widget(make_label(item["title"], 15, ACCENT, 30, True))
            self.items.add_widget(make_label(item["message"] + "\n" + item["date"], 12, MUTED, 62))


def hash_password(password):
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), 200000).hex()
    return {"salt": salt, "hash": digest, "iterations": 200000}


def verify_password(password, stored):
    try:
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(stored["salt"]), int(stored["iterations"])).hex()
        return secrets.compare_digest(digest, stored["hash"])
    except (KeyError, ValueError, TypeError):
        return False


def open_url(url):
    try:
        webbrowser.open(url)
    except Exception:
        pass


class TrustLensApp(App):
    def build(self):
        self.title = "TrustLens"
        self.current_email = ""
        self.users = {}
        self.saved = {}
        self.notices = []
        self.load_data()
        manager = ScreenManager()
        manager.add_widget(LoginScreen(name="login"))
        manager.add_widget(HomeScreen(name="home"))
        manager.add_widget(OpportunitiesScreen(name="opportunities"))
        manager.add_widget(SavedScreen(name="saved"))
        manager.add_widget(IntegrationsScreen(name="integrations"))
        manager.add_widget(NotificationsScreen(name="notifications"))
        return manager

    def data_path(self, filename):
        return os.path.join(self.user_data_dir, filename)

    def read_json(self, filename, default):
        try:
            with open(self.data_path(filename), "r", encoding="utf-8") as handle:
                return json.load(handle)
        except (OSError, ValueError):
            return default

    def write_json(self, filename, value):
        os.makedirs(self.user_data_dir, exist_ok=True)
        temp = self.data_path(filename + ".tmp")
        with open(temp, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
        os.replace(temp, self.data_path(filename))

    def load_data(self):
        self.users = self.read_json("users.json", {})
        self.saved = self.read_json("saved.json", {})
        self.notices = self.read_json("notifications.json", [])

    def save_users(self):
        self.write_json("users.json", self.users)

    def save_opportunity(self, item):
        email = self.current_email
        if not email:
            return
        entries = self.saved.setdefault(email, [])
        if not any(entry.get("url") == item["url"] for entry in entries):
            entries.append(item)
            self.write_json("saved.json", self.saved)
            self.add_notice("Opportunity saved", item["title"] + " was added to your saved list.")
        self.root.current = "saved"

    def add_notice(self, title, message):
        self.notices.append({"title": title, "message": message, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
        self.notices = self.notices[-100:]
        self.write_json("notifications.json", self.notices)

    def open_home(self):
        self.root.current = "home"


if __name__ == "__main__":
    TrustLensApp().run()
