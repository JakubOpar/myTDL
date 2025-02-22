import sqlite3

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from database import initialize_database, add_category, delete_category, get_categories, get_tasks, delete_task, \
    update_task
from kivy.lang import Builder
from kivy.core.window import Window
from dynamic_categories import generate_categories
from kivy.clock import Clock
from dynamic_tasks import generate_tasks


Window.size = (450, 600)

Window.top = 100
Window.left = 100
Window.fullscreen = False

class MainMenu(Screen):
    pass


class AddCategoryScreen(Screen):
    pass


class DeleteCategoryScreen(Screen):
    pass


class CategoryListScreen(Screen):
    pass


class TaskManagementScreen(Screen):
    pass


class LoadingScreen(Screen):
    pass

class EditTaskScreen(Screen):
    pass

class TaskManagerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_category = None  # Nowa zmienna przechowująca wybraną kategorię

    def build(self):
        print("Inicjalizacja bazy danych...")
        initialize_database()

        self.sm = ScreenManager()

        print("Ładowanie aplikacji...")
        Builder.load_file("views.kv")

        # Dodanie ekranów do ScreenManager
        self.sm.add_widget(LoadingScreen(name='loading'))
        self.sm.add_widget(MainMenu(name='main_menu'))
        self.sm.add_widget(AddCategoryScreen(name='add_category'))
        self.sm.add_widget(DeleteCategoryScreen(name='delete_category'))
        self.sm.add_widget(CategoryListScreen(name='category_list'))
        self.sm.add_widget(TaskManagementScreen(name='task_management'))  # WAŻNE!
        self.sm.add_widget(EditTaskScreen(name='edit_task'))

        print("Dodane ekrany:", [screen.name for screen in self.sm.screens])

        # Sprawdzenie, czy `task_management` jest w ScreenManager
        if 'task_management' not in [screen.name for screen in self.sm.screens]:
            print("⚠️ Ekran 'task_management' NIE został poprawnie dodany!")

        self.sm.current = 'loading'
        Clock.schedule_once(lambda dt: self.show_category_list_screen(), 0.3)

        return self.sm

    def show_main_menu(self):
        print("Przechodzenie do ekranu kategorii...")
        self.show_category_list_screen()

    def show_add_category_screen(self):
        self.sm.current = 'add_category'

    def show_delete_category_screen(self):
        self.sm.current = 'delete_category'
        screen = self.sm.get_screen('delete_category')

        categories = self.get_category_list()

        screen.ids.category_spinner.values = categories
        screen.ids.category_spinner.text = "Wybierz kategorię"

    def show_category_list_screen(self):
        print("Przełączanie na ekran ładowania...")
        self.sm.current = 'loading'

        Clock.schedule_once(lambda dt: self._load_category_list(), 0.3)
        print("Ekran ładowania aktywowany, zaraz załadujemy listę kategorii.")

    def _load_category_list(self):
        print("Wywołanie show_category_list_screen...")  # Debugowanie
        self.sm.current = 'category_list'

        try:
            category_list_layout = self.sm.get_screen('category_list').ids.category_list
        except Exception as e:
            print("Błąd przy pobieraniu ekranu kategorii:", e)
            return

        print("Pobrano layout kategorii:", category_list_layout)  # Debugowanie

        categories = [category[1] for category in get_categories()]
        print("Pobrane kategorie do wyświetlenia:", categories)  # Debugowanie

        generate_categories(
            category_list_layout,
            categories,
            self.show_task_management_screen,  # Prawidłowe przekazanie funkcji
            self.delete_category
        )

    def show_task_management_screen(self, category_name):
        """Przechodzi do ekranu zarządzania zadaniami i zapisuje wybraną kategorię."""

        print(f"🟢 Kliknięto przycisk w kategorii: {category_name}")  # Sprawdzamy co faktycznie przychodzi
        print(f"🔄 Przed zmianą: self.selected_category = {self.selected_category}")  # Sprawdzenie, co było wcześniej

        # Poprawne przypisanie wybranej kategorii
        self.selected_category = category_name
        print(
            f"✅ Po zmianie: self.selected_category = {self.selected_category}")  # Sprawdzenie, czy zmiana faktycznie nastąpiła

        self.sm.current = 'loading'
        Clock.schedule_once(lambda dt: self._load_task_management_screen(), 0.3)

    def _load_task_management_screen(self):
        """Ładuje zadania dla wybranej kategorii."""
        if not self.selected_category:
            print("🔴 BŁĄD: self.selected_category jest None!")
            return

        category_name = self.selected_category  # Używamy zapisanej kategorii
        print(f"📌 Ładowanie ekranu zarządzania zadaniami dla kategorii: {category_name}")

        self.sm.current = 'task_management'
        screen = self.sm.get_screen('task_management')
        screen.ids.category_label.text = f"Zadania dla kategorii: {category_name}"

        task_list_layout = screen.ids.task_list
        task_list_layout.clear_widgets()

        tasks = get_tasks()
        category_tasks = [task for task in tasks if task[-1] == category_name]

        print(f"✅ Zadania przypisane do {category_name}: {category_tasks}")

        generate_tasks(
            task_list_layout,
            category_tasks,
            lambda task_id, cat_name: self.edit_task(task_id, cat_name),
            lambda task_id, cat_name: self.delete_task(task_id, cat_name)
        )

        print(f"📌 Załadowano {len(category_tasks)} zadań dla kategorii {category_name}")

    def get_category_list(self):
        categories = get_categories()
        return [category[1] for category in categories]

    def add_category(self, name):
        if not name.strip():
            print("Nazwa kategorii nie może być pusta.")
            return
        try:
            self.sm.current = 'loading'
            Clock.schedule_once(lambda dt: self._add_category_logic(name), 0.3)
        except ValueError as e:
            print(f"Error: {e}")

    def _add_category_logic(self, name):
        add_category(name)
        print(f"Kategoria '{name}' została dodana.")
        self.show_category_list_screen()

    def delete_category(self, name):
        try:
            self.sm.current = 'loading'
            Clock.schedule_once(lambda dt: self._delete_category_logic(name), 0.3)
        except ValueError as e:
            print(f"Error: {e}")

    def _delete_category_logic(self, name):
        delete_category(name)
        print(f"Kategoria '{name}' została usunięta.")
        self.show_category_list_screen()

    def manage_tasks(self, category_name):
        self.show_task_management_screen(category_name)

    def delete_task(self, task_id, category_name):
        """Usuwa zadanie i odświeża ekran zarządzania zadaniami."""
        print(f"🗑 Usuwanie zadania ID: {task_id} z kategorii {category_name}")

        delete_task(task_id)  # Usunięcie zadania z bazy danych

        # Odświeżenie ekranu z listą zadań
        self.show_task_management_screen(category_name)

    def edit_task(self, task_id, category_name):
        """Przechodzi do ekranu edycji zadania."""
        print(f"✎ Edycja zadania ID: {task_id} w kategorii {category_name}")

        self.sm.current = 'loading'
        Clock.schedule_once(lambda dt: self._load_edit_task_screen(task_id, category_name), 0.3)

    def _load_edit_task_screen(self, task_id, category_name):
        """Ładuje ekran edycji zadania."""
        print(f"📌 Ładowanie ekranu edycji dla zadania ID: {task_id} (Kategoria: {category_name})")

        self.sm.current = 'edit_task'
        screen = self.sm.get_screen('edit_task')

        # Pobranie danych zadania z bazy
        tasks = get_tasks()
        task_data = next((t for t in tasks if t[0] == task_id), None)

        if not task_data:
            print(f"⚠️ Nie znaleziono zadania ID {task_id}")
            return

        print(f"✅ Załadowano dane zadania: {task_data}")  # Debugowanie

        # Wypełnienie pól edycyjnych
        screen.ids.task_name.text = str(task_data[1]) if task_data[1] else ""
        screen.ids.task_priority.text = str(task_data[2]) if task_data[2] else ""
        screen.ids.task_date.text = str(task_data[3]) if task_data[3] else ""
        screen.ids.task_reminder.text = str(task_data[4]) if task_data[4] else ""
        screen.ids.task_description.text = str(task_data[5]) if task_data[5] else ""

        print(f"📌 Wpisano do pól: {screen.ids.task_name.text}, {screen.ids.task_priority.text}, {screen.ids.task_date.text}")

        # Przypisanie funkcji do przycisku zapisu
        screen.ids.save_button.bind(
            on_press=lambda instance: self.save_task_changes(
                task_id,
                screen.ids.task_name.text,
                screen.ids.task_priority.text,
                screen.ids.task_date.text,
                screen.ids.task_reminder.text,
                screen.ids.task_description.text,
                category_name
            )
        )

        # Przypisanie funkcji do przycisku powrotu
        screen.ids.cancel_button.bind(
            on_press=lambda instance: self.show_task_management_screen(category_name)
        )


    def save_task_changes(self, task_id, name, priority, task_date, reminder, description, category_name):
        """Zapisuje zmiany w zadaniu i wraca do ekranu z listą zadań."""
        print(f"💾 Zapisywanie zmian w zadaniu ID {task_id}")

        try:
            update_task(
                task_id,
                name=name,
                priority=int(priority),
                task_date=task_date,
                reminder=reminder,
                description=description,
                category_name=category_name
            )
            print("✅ Zmiany zapisane.")
        except Exception as e:
            print(f"❌ Błąd podczas zapisu zmian: {e}")

        # Powrót do listy zadań po zapisaniu
        self.show_task_management_screen(category_name)



if __name__ == "__main__":
    TaskManagerApp().run()
