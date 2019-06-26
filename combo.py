"""
This is a simple example of how to use suggestion text.
In this example you setup a word_list at the begining. In this case
'the the quick brown fox jumps over the lazy old dog'. This list along
with any new word written word in the textinput is available as a
suggestion when you are typing. You can press tab to auto complete the text.
"""
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from textwrap import dedent


class MyTextInput(TextInput):
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        """ Add support for tab as an 'autocomplete' using the suggestion text.
        """
        if self.suggestion_text and keycode[1] == 'tab':
            self.insert_text(self.suggestion_text + ' ')
            return True
        return super(MyTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)


class MyApp(App):

    word_list = (
        'The quick brown fox jumps jani laci laló over the lazy old dog').split(' ')

    def on_text(self, instance, value):
        """ Include all current text from textinput into the word list to
        emulate the same kind of behavior as sublime text has.
        """
        self.root.suggestion_text = ''
        word_list = list(set(
            self.word_list + value[:value.rfind(' ')].split(' ')))
        val = value[value.rfind(' ') + 1:]
        if not val:
            return
        try:
            # grossly inefficient just for demo purposes
            word = [word for word in word_list
                    if word.startswith(val)][0][len(val):]
            if not word:
                return
            self.root.suggestion_text = word
        except IndexError:
            print ('Index Error.')

    def build(self):
        text_input = Builder.load_string(dedent('''
            MyTextInput
                readonly: False
                multiline: False
        '''))
        text_input.bind(text=self.on_text)
        return text_input

if __name__ == "__main__":
    MyApp().run()