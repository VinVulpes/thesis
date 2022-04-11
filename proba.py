from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout  # кнопки должны быть внутри слоя
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from kivy.core.window import Window
from random import randint

Window.size = (300, 200)
Window.clearcolor = (255 / 255, 186 / 255, 3 / 255, 1)
Window.title = "Приложение"


class MyApp(App):
    # Чтобы обратиться к обьекту из другого метода, нужно обьявить что она принадлежит всему классу
    def __init__(self):
        super().__init__()
        self.label = Label(text='Первое окно!')
        self.path_log_file = TextInput(hint_text='Введите путь к лог файлу', multiline=False)

    def btn_new_bd_pressed(self, *args):  # Получение доп аргументов
        popup = Popup(title='new_bd_pressed',
                      content=self.path_log_file,
                      size=(400, 400))
        popup.open()
        btn_back = Button(text='Back')

    def btn_ex_bd_pressed(self, *args):
        popup = Popup(title='ex_bd_pressed',
                      content=Window,
                      size_hint=(None, None), size=(400, 400))
        popup.open()

    def btn_back(self,*args):
        popup = Popup(title='ex_bd_pressed',
                      content=Window,
                      size_hint=(None, None), size=(400, 400))
        popup.open()

    def build(self):
        box = BoxLayout(orienatation = 'vertical')
        btn_new_bd = Button(text='New BD')
        btn_ex_bd = Button(text='Open existing')
        btn_new_bd.bind(on_press=self.btn_new_bd_pressed)
        btn_ex_bd.bind(on_press=self.btn_ex_bd_pressed)
        btn_back.bind(on_press=self.btn_back)
        box.add_widget(btn_new_bd)
        box.add_widget(btn_ex_bd)
        return box


if __name__ == "__main__":
    MyApp().run()
# Словарь
"""
        fl = 0 
        for i in range(6):
            for j in d.copy(): 
                if pr_text[i] == j:
                    d[j][1] += 1
                    fl = 1
                    break
            if fl == 0:
                d.update({pr_text[i]: [i, 1]})
            fl = 0
#Вывод статистики - какие сообщения, их тип и сколько их всего
for key, val in d.items():
    print('Сообщение: ', key, 'Тип: ', val[0], 'Встретилось: ', val[1],' раз')
"""
