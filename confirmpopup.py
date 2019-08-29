from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label

class ConfirmPopup(GridLayout):
    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super(ConfirmPopup, self).__init__(**kwargs)
        self.cols = 1
        self.cimke = Label()
        self.cimke.text = 'Do You Love Kivy?'
        self.popup_background = GridLayout()
        self.popup_background.cols = 2
        self.popup_background.size_hint_y = None
        self.popup_background.height = '44sp'
        self.yes_gomb = Button()
        self.yes_gomb.text = "Yes"
        self.yes_gomb.bind(on_release=lambda a: self.dispatch('on_answer', 'yes'))
        self.no_gomb = Button()
        self.no_gomb.text = "No"
        self.no_gomb.bind(on_release=lambda a: self.dispatch('on_answer', 'no'))
        self.popup_background.add_widget(self.yes_gomb)
        self.popup_background.add_widget(self.no_gomb)
        self.add_widget(self.cimke)
        self.add_widget(self.popup_background)

    def on_answer(self, *args):
        pass

class SajatPopup():
    def __init__(self, **kwargs):
        super(SajatPopup, self).__init__(**kwargs)
        content = ConfirmPopup()
        content.bind(on_answer=self._on_answer)
        self.popup = Popup(title="Mit akarsz?",
                           content=content,
                           size_hint=(None, None),
                           size=(480, 400),
                           auto_dismiss=False)

    def _on_answer(self, instance, answer):
        print("USER ANSWER: ", repr(answer))
        self.popup.dismiss()

class PopupTest(App):
    def build(self):
        self.felugro = SajatPopup()
        self.felugro.popup.open()

if __name__ == '__main__':
    PopupTest().run()