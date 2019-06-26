from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.lang import Builder
import sqlite3, os



class TesztScreen(GridLayout):

    def __init__(self, **kwargs):
        super(TesztScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        temptext = ''
        dbfile = 'adatbazis.db'
        db_exist = os.path.exists(dbfile)
        if db_exist:
            self.conn = sqlite3.connect(dbfile)
            self.kurzor = self.conn.cursor()
        self.kurzor.execute("select * from players")
        sor2 = self.kurzor.fetchall()
        for sor in sor2:
            temptext += sor[1] + " "
        self.player_hint = temptext.split(' ')
        self.username.suggestion_text = ''

        self.add_widget(self.username)


class MyApp(App):
    def build(self):

        return TesztScreen()

if __name__ == '__main__':
    MyApp().run()
