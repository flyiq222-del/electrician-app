from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(text="[b]СПРАВОЧНИК ЭЛЕКТРИКА[/b]", markup=True, font_size=24, size_hint_y=None, height=50))
        
        btn1 = Button(text="1. Закон Ома и Мощность", font_size=18)
        btn1.bind(on_press=lambda x: self.manager.switch_to(OhmScreen()))
        layout.add_widget(btn1)
        
        btn2 = Button(text="2. Выбор сечения кабеля (ПУЭ)", font_size=18)
        btn2.bind(on_press=lambda x: self.manager.switch_to(CableScreen()))
        layout.add_widget(btn2)
        
        btn3 = Button(text="3. Падение напряжения", font_size=18)
        btn3.bind(on_press=lambda x: self.manager.switch_to(VoltageDropScreen()))
        layout.add_widget(btn3)
        
        btn4 = Button(text="4. Схемы подключения", font_size=18)
        btn4.bind(on_press=lambda x: self.manager.switch_to(SchemesScreen()))
        layout.add_widget(btn4)
        
        self.add_widget(layout)


class OhmScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout.add_widget(Label(text="Расчет по закону Ома", font_size=20, size_hint_y=None, height=40))
        
        self.mode_spinner = Spinner(text='U и R (Найти I, P)', values=('U и R (Найти I, P)', 'P и U (Найти I, R)', 'I и R (Найти U, P)'), size_hint_y=None, height=44)
        layout.add_widget(self.mode_spinner)
        
        self.val1_input = TextInput(hint_text='Введите первое значение (U/P/I)', multiline=False, size_hint_y=None, height=44)
        layout.add_widget(self.val1_input)
        
        self.val2_input = TextInput(hint_text='Введите второе значение (R/U/R)', multiline=False, size_hint_y=None, height=44)
        layout.add_widget(self.val2_input)
        
        calc_btn = Button(text="Рассчитать", size_hint_y=None, height=50)
        calc_btn.bind(on_press=self.calculate)
        layout.add_widget(calc_btn)
        
        self.result_label = Label(text="Результат появится здесь", font_size=16)
        layout.add_widget(self.result_label)
        
        back_btn = Button(text="Назад в меню", size_hint_y=None, height=44)
        back_btn.bind(on_press=lambda x: self.manager.switch_to(MainMenuScreen()))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        
    def calculate(self, instance):
        try:
            v1 = float(self.val1_input.text)
            v2 = float(self.val2_input.text)
            mode = self.mode_spinner.text
            
            if 'U и R' in mode:
                i = v1 / v2
                p = v1 * i
                self.result_label.text = f"Ток (I): {i:.2f} А\nМощность (P): {p:.2f} Вт"
            elif 'P и U' in mode:
                i = v1 / v2
                r = v2 / i
                self.result_label.text = f"Ток (I): {i:.2f} А\nСопротивление (R): {r:.2f} Ом"
            elif 'I и R' in mode:
                u = v1 * v2
                p = u * v1
                self.result_label.text = f"Напряжение (U): {u:.2f} В\nМощность (P): {p:.2f} Вт"
        except ValueError:
            self.result_label.text = "Ошибка: введите числа корректно!"


class CableScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout.add_widget(Label(text="Выбор сечения кабеля (медь, ПУЭ)", font_size=20, size_hint_y=None, height=40))
        
        self.current_input = TextInput(hint_text='Ток нагрузки (А)', multiline=False, size_hint_y=None, height=44)
        layout.add_widget(self.current_input)
        
        self.type_spinner = Spinner(text='Скрытая прокладка / в трубе', values=('Скрытая прокладка / в трубе', 'Открытая прокладка'), size_hint_y=None, height=44)
        layout.add_widget(self.type_spinner)
        
        calc_btn = Button(text="Подобрать сечение", size_hint_y=None, height=50)
        calc_btn.bind(on_press=self.calculate)
        layout.add_widget(calc_btn)
        
        self.result_label = Label(text="Результат появится здесь", font_size=16)
        layout.add_widget(self.result_label)
        
        back_btn = Button(text="Назад в меню", size_hint_y=None, height=44)
        back_btn.bind(on_press=lambda x: self.manager.switch_to(MainMenuScreen()))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        
    def calculate(self, instance):
        try:
            current = float(self.current_input.text)
            is_hidden = 'Скрытая' in self.type_spinner.text
            
            pue_table = [
                (1.5, 19, 23),
                (2.5, 27, 30),
                (4.0, 38, 41),
                (6.0, 50, 50),
                (10.0, 70, 80),
                (16.0, 85, 100),
                (25.0, 115, 130),
                (35.0, 135, 155),
                (50.0, 175, 210)
            ]
            
            selected_section = None
            for section, hidden_cur, open_cur in pue_table:
                allowed_cur = hidden_cur if is_hidden else open_cur
                if allowed_cur >= current:
                    selected_section = section
                    break
                    
            if selected_section:
                self.result_label.text = f"Рекомендуемое сечение: {selected_section} мм²"
            else:
                self.result_label.text = "Требуется сечение > 50 мм²"
        except ValueError:
            self.result_label.text = "Ошибка ввода!"


class VoltageDropScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout.add_widget(Label(text="Расчет падения напряжения", font_size=20, size_hint_y=None, height=40))
        
        self.cur_input = TextInput(hint_text='Ток (А)', multiline=False, size_hint_y=None, height=44)
        layout.add_widget(self.cur_input)
        
        self.len_input = TextInput(hint_text='Длина линии в одну сторону (м)', multiline=False, size_hint_y=None, height=44)
        layout.add_widget(self.len_input)
        
        self.sec_input = TextInput(hint_text='Сечение кабеля (мм²)', multiline=False, size_hint_y=None, height=44)
        layout.add_widget(self.sec_input)
        
        self.mat_spinner = Spinner(text='Медь', values=('Медь', 'Алюминий'), size_hint_y=None, height=44)
        layout.add_widget(self.mat_spinner)
        
        calc_btn = Button(text="Рассчитать падение", size_hint_y=None, height=50)
        calc_btn.bind(on_press=self.calculate)
        layout.add_widget(calc_btn)
        
        self.result_label = Label(text="Результат появится здесь", font_size=16)
        layout.add_widget(self.result_label)
        
        back_btn = Button(text="Назад в меню", size_hint_y=None, height=44)
        back_btn.bind(on_press=lambda x: self.manager.switch_to(MainMenuScreen()))
        layout.add_widget(layout_item := back_btn) # layout_item cleanup trick if needed, standard add below
        layout.add_widget(back_btn)
        
        self.add_widget(layout)

    def calculate(self, instance):
        try:
            current = float(self.cur_input.text)
            length = float(self.len_input.text)
            section = float(self.sec_input.text)
            rho = 0.0175 if self.mat_spinner.text == 'Медь' else 0.028
            
            voltage_drop = (2 * length * current * rho) / section
            percent_drop = (voltage_drop / 220.0) * 100
            
            status = "В норме (<5%)" if percent_drop <= 5 else "Превышает 5%!"
            self.result_label.text = f"Падение: {voltage_drop:.2f} В ({percent_drop:.2f}%)\nСтатус: {status}"
        except ValueError:
            self.result_label.text = "Ошибка ввода!"


class SchemesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout.add_widget(Label(text="Схемы подключения", font_size=20, size_hint_y=None, height=40))
        
        self.scheme_spinner = Spinner(
            text='Выберите схему', 
            values=('Розетка с заземлением', 'Одноклавишный выключатель', 'Проходные выключатели'), 
            size_hint_y=None, height=44
        )
        self.scheme_spinner.bind(text=self.show_scheme_text)
        layout.add_widget(self.scheme_spinner)
        
        scroll = ScrollView()
        self.desc_label = Label(text="Выберите схему из списка выше, чтобы увидеть описание и коммутацию.", size_hint_y=None, font_size=14)
        self.desc_label.bind(texture_size=lambda s, t: setattr(s, 'height', t[1]))
        scroll.add_widget(self.desc_label)
        layout.add_widget(scroll)
        
        back_btn = Button(text="Назад в меню", size_hint_y=None, height=44)
        back_btn.bind(on_press=lambda x: self.manager.switch_to(MainMenuScreen()))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
        
    def show_scheme_text(self, spinner, text):
        if text == 'Розетка с заземлением':
            self.desc_label.text = "🔌 Розетка с заземлением:\n\n• Фаза (L) -> Левый контакт\n• Ноль (N) -> Правый контакт\n• Земля (PE) -> Центральный усик"
        elif text == 'Одноклавишный выключатель':
            self.desc_label.text = "💡 Одноклавишный выключатель:\n\n• В щите разрывается ФАЗА (L).\n• Фаза заходит на вход выключателя [COM], с выхода идет на лампу.\n• Ноль (N) идет напрямую к лампе."
        elif text == 'Проходные выключатели':
            self.desc_label.text = "🔄 Проходные (управление из 2 мест):\n\n• Используются 2 переключателя на 3 контакта.\n• Фаза заходит на общий вход первого переключателя.\n• Две перемычки соединяют выходы 1-го и 2-го переключателей.\n• Общий выход второго идет на светильник."


class ElectricianApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen())
        return sm

if __name__ == '__main__':
    ElectricianApp().run()
