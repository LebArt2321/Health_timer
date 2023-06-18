from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ListProperty
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ObjectProperty
from kivy.animation import Animation
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import mysql.connector
from plyer import notification
from plyer.utils import platform

Window.size = (350, 600)


def connect_to_database():
    conn = mysql.connector.connect(
        host='sql7.freesqldatabase.com',
        user='sql7624599',
        password='VcepQuEmEW',
        database='sql7624599'
    )
    create_users_table(conn)  # Создание таблицы пользователей при подключении к базе данных
    return conn


def create_users_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INT PRIMARY KEY AUTO_INCREMENT,
                   username VARCHAR(255),
                   password VARCHAR(255),
                   name VARCHAR(255),
                   age INT,
                   blood_group VARCHAR(255),
                   diseases VARCHAR(255),
                   allergies VARCHAR(255),
                   weight INT,
                   email VARCHAR(255))''')

    # Добавьте эту строку для сохранения изменений
    conn.commit()


class LoginScreen(Screen):
    def login(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        if username and password:  # Проверка, что поля ввода не пустые
            conn = connect_to_database()
            cursor = conn.cursor()

            # Выполнение запроса для проверки данных авторизации
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))

            result = cursor.fetchone()

            conn.close()

            # Проверка результатов запроса
            if result is not None:
                app = MDApp.get_running_app()
                app.username = username  # Установка атрибута username в экземпляре приложения
                self.manager.current = "timer"  # Переход на экран таймера после успешной авторизации
            else:
                self.show_error_dialog("Ошибка авторизации. Проверьте правильность введенных данных.")
        else:
            # Вывод сообщения об ошибке, если поля ввода пустые
            self.show_error_dialog("Пожалуйста, заполните все поля.")

    def show_error_dialog(self, message):
        close_button = MDFlatButton(text='Ок', on_release=self.close_error_dialog)

        content_box = MDBoxLayout(orientation='vertical', adaptive_height=True)
        content_box.add_widget(MDTextField(text=message, readonly=True))

        self.dialog = MDDialog(type="custom", content_cls=content_box, buttons=[close_button])
        self.dialog.open()

    def close_error_dialog(self, obj):
        self.dialog.dismiss()


class RegisterScreen(Screen):
    def register(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text
        name = self.ids.name_input.text
        age = self.ids.age_input.text
        blood_group = self.ids.blood_group_input.text
        diseases = self.ids.diseases_input.text
        allergies = self.ids.allergies_input.text
        weight = self.ids.weight_input.text

        if username and password and name and age and blood_group and diseases and allergies and weight:
            conn = connect_to_database()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if existing_user is None:
                cursor.execute(
                    "INSERT INTO users (username, password, name, age, blood_group, diseases, allergies, weight) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (username, password, name, age, blood_group, diseases, allergies, weight))
                conn.commit()

                self.manager.current = "login"
            else:
                self.show_error_dialog("Пользователь с таким именем уже существует.")

            conn.close()
        else:
            self.show_error_dialog("Пожалуйста, заполните все поля.")

    def show_error_dialog(self, message):
        close_button = MDFlatButton(text='Ок', on_release=self.close_error_dialog)

        content_box = MDBoxLayout(orientation='vertical', adaptive_height=True)
        content_box.add_widget(MDTextField(text=message, readonly=True))

        self.dialog = MDDialog(type="custom", content_cls=content_box, buttons=[close_button])
        self.dialog.open()

    def close_error_dialog(self, obj):
        self.dialog.dismiss()


class LKScreen(Screen):
    name_label = StringProperty("")
    age_label = StringProperty("")
    blood_group_label = StringProperty("")
    allergies_label = StringProperty("")
    diseases_label = StringProperty("")
    weight_label = StringProperty("")

    def on_pre_enter(self):
        app = MDApp.get_running_app()
        username = app.username  # Предполагая, что вы храните имя пользователя в экземпляре приложения

        conn = connect_to_database()
        cursor = conn.cursor()

        # Получение данных пользователя
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()

        conn.close()

        if user_data:
            self.name_label = user_data[3]  # Предполагая, что имя находится на индексе 3
            self.age_label = str(user_data[4])  # Предполагая, что возраст находится на индексе 4
            self.blood_group_label = user_data[5]  # Предполагая, что группа крови находится на индексе 5
            self.allergies_label = user_data[7]  # Предполагая, что аллергии находятся на индексе 7
            self.diseases_label = user_data[6]  # Предполагая, что болезни находятся на индексе 6
            self.weight_label = str(user_data[8])  # Предполагая, что вес находится на индексе 8


class ADDLKScreen(Screen):
    name_input = ObjectProperty(None)
    age_input = ObjectProperty(None)
    blood_group_input = ObjectProperty(None)
    diseases_input = ObjectProperty(None)
    allergies_input = ObjectProperty(None)
    weight_input = ObjectProperty(None)

    def save_data(self):
        app = MDApp.get_running_app()
        username = app.username  # Предполагая, что вы храните имя пользователя в экземпляре приложения

        name = self.ids.name_input.text.strip()  # Используем strip() для удаления возможных пробелов в начале и конце строки
        age = self.ids.age_input.text.strip()
        blood_group = self.ids.blood_group_input.text.strip()
        diseases = self.ids.diseases_input.text.strip()
        allergies = self.ids.allergies_input.text.strip()
        weight = self.ids.weight_input.text.strip()

        # Получаем текущие данные пользователя из базы данных
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT name, age, blood_group, diseases, allergies, weight FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        conn.close()

        # Если поле пустое, используем текущие данные пользователя из базы данных
        name = name or user_data[0]
        age = int(age) if age else user_data[1]
        blood_group = blood_group or user_data[2]
        diseases = diseases or user_data[3]
        allergies = allergies or user_data[4]
        weight = float(weight) if weight else user_data[5]

        conn = connect_to_database()
        cursor = conn.cursor()

        # Обновление данных пользователя в базе данных
        cursor.execute(
            "UPDATE users SET name = %s, age = %s, blood_group = %s, diseases = %s, allergies = %s, weight = %s WHERE username = %s",
            (name, age, blood_group, diseases, allergies, weight, username))

        conn.commit()
        conn.close()

        self.manager.current = "LK"  # Переход на экран с данными пользователя


    def show_error_dialog(self, message):
        close_button = MDFlatButton(text='Ок', on_release=self.close_error_dialog)

        content_box = MDBoxLayout(orientation='vertical', adaptive_height=True)
        content_box.add_widget(MDTextField(text=message, readonly=True))

        self.dialog = MDDialog(type="custom", content_cls=content_box, buttons=[close_button])
        self.dialog.open()

    def close_error_dialog(self, obj):
        self.dialog.dismiss()


class TimerScreen(Screen):
    timers = []
    timer_height = 0.4
    name_label = StringProperty("")

    def on_pre_enter(self):
        app = MDApp.get_running_app()
        username = app.username  # Предполагая, что вы храните имя пользователя в экземпляре приложения

        conn = connect_to_database()
        cursor = conn.cursor()

        # Получение данных пользователя
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()

        conn.close()

        if user_data:
            self.name_label = user_data[3]  # Предполагая, что имя находится на индексе 3

    def start_timer(self, medication_name, hours, minutes):
        if not self.ids.circular_progress_bar.is_active():
            self.ids.circular_progress_bar.start_timer(medication_name, hours, minutes)
        else:
            timer = HorizontalProgressBar()
            timer.set_value = 100
            timer.start_timer(hours, minutes)
            timer.medication_name = medication_name
            self.add_timer(timer)

    def add_timer(self, timer):
        self.timers.append(timer)
        self.update_timers()

    def remove_timer(self, timer):
        self.timers.remove(timer)
        self.update_timers()

    def update_timers(self):
        timers_layout = self.ids.timers_layout
        timers_layout.clear_widgets()
        for timer in self.timers:
            timers_layout.add_widget(timer)


class WindowManager(ScreenManager):
    pass


class MyApp(MDApp):
    username = ""  # Добавляем атрибут username

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        conn = connect_to_database()
        return WindowManager()

    def show_add_medication_dialog(self):
        close_button = MDFlatButton(text='Cancel', on_release=self.close_dialog)
        start_button = MDFlatButton(text='Start', on_release=self.start_timer_from_dialog)

        self.medication_name_input = MDTextField(hint_text='Medication Name', size_hint_y=None, height=dp(35))
        self.hours_input = MDTextField(
            hint_text='Hours', input_filter='int', max_text_length=2, size_hint_y=None, height=dp(35), text='0'
        )
        self.minutes_input = MDTextField(
            hint_text='Minutes', input_filter='int', max_text_length=2, size_hint_y=None, height=dp(35), text='0'
        )

        content_box = MDBoxLayout(orientation='vertical', adaptive_height=True)
        content_box.add_widget(self.medication_name_input)
        content_box.add_widget(self.hours_input)
        content_box.add_widget(self.minutes_input)

        self.dialog = MDDialog(
            type="custom",
            content_cls=content_box,
            buttons=[close_button, start_button],
        )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def start_timer_from_dialog(self, obj):
        medication_name = self.medication_name_input.text
        hours = int(self.hours_input.text)
        minutes = int(self.minutes_input.text)

        if not self.root.ids.timer_screen.ids.circular_progress_bar.is_active():
            self.root.ids.timer_screen.start_timer(medication_name, hours, minutes)
            self.root.ids.timer_screen.ids.medication_label.text = medication_name
        else:
            timer = HorizontalProgressBar()
            timer.set_value = 100
            timer.start_timer(hours, minutes)
            timer.medication_name = medication_name
            self.root.ids.timer_screen.add_timer(timer)

        self.dialog.dismiss()

    def send_notification(self, title, message):
        if platform == 'win':
            notification.notify(
                title=title,
                message=message,
                app_icon=None,
                timeout=10,
            )
        elif platform == 'linux':
            notification.notify(
                title=title,
                message=message,
                app_icon=None,
                timeout=10,
            )
        elif platform == 'android':
            notification.notify(
                title=title,
                message=message,
                app_icon=None,
                timeout=10,
            )
        else:
            print("Platform not supported for notifications.")

    # def on_stop(self):
    #     # Остановка всех таймеров при выходе из приложения
    #     for timer in self.root.ids.timer_screen.timers:
    #         timer.stop_timer()


class CircularProgressBar(AnchorLayout):
    medication_name = StringProperty('')
    set_value = NumericProperty(100)
    value = NumericProperty(0)
    bar_width = NumericProperty(7)
    duration = NumericProperty(1.5)
    timer_value = NumericProperty(0)
    timer = None
    active_timer = BooleanProperty(False)

    def start_timer(self, medication_name, hours, minutes):
        total_minutes = (hours * 60) + minutes
        total_seconds = total_minutes * 60
        self.stop_timer()
        self.timer_value = total_seconds
        self.timer = Animation(set_value=0, duration=self.timer_value)
        self.timer.bind(on_progress=self.update_timer_progress, on_complete=self.update_timer_complete)
        self.timer.start(self)
        self.active_timer = True

    def update_timer_progress(self, animation, widget, progress):
        self.ids.timer_label.text = self.format_time(int((1 - progress) * self.timer_value))

    def update_timer_complete(self, animation, widget):
        self.stop_timer()
        self.active_timer = False
        app = MDApp.get_running_app()
        app.send_notification("Medication Reminder", f"Time to take {self.medication_name}")
        app.root.ids.timer_screen.ids.medication_label.text = ''

    def is_active(self):
        return self.active_timer

    def stop_timer(self):
        if self.timer:
            self.timer.stop(self)
            self.timer = None
            self.timer_value = 0
            self.set_value = 100
            self.ids.timer_label.text = self.format_time(self.timer_value)

    @staticmethod
    def format_time(seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


class HorizontalProgressBar(AnchorLayout):
    medication_name = StringProperty('')
    set_value = NumericProperty(100)
    value = NumericProperty(0)
    bar_width = NumericProperty(5)
    duration = NumericProperty(1.5)
    timer_value = NumericProperty(0)
    timer = None

    def start_timer(self, hours, minutes):
        total_minutes = (hours * 60) + minutes
        total_seconds = total_minutes * 60
        self.stop_timer()
        self.timer_value = total_seconds
        self.timer = Animation(set_value=0, duration=self.timer_value)
        self.timer.bind(on_progress=self.update_timer_progress, on_complete=self.update_timer_complete)
        self.timer.start(self)

    def update_timer_progress(self, animation, widget, progress):
        self.ids.timer_label.text = self.format_time(int((1 - progress) * self.timer_value))

    def update_timer_complete(self, animation, widget):
        self.stop_timer()
        app = MDApp.get_running_app()
        app.root.ids.timer_screen.remove_timer(self)
        app.send_notification("Medication Reminder", f"Time to take {self.medication_name}")

    def stop_timer(self):
        if self.timer:
            self.timer.stop(self)
            self.timer = None
            self.timer_value = 0
            self.value = 0
            self.set_value = 100
            self.ids.timer_label.text = self.format_time(self.timer_value)

    @staticmethod
    def format_time(seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


if __name__ == '__main__':
    MyApp().run()
