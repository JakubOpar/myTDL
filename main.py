from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from database import initialize_database, add_category, delete_category, get_categories
from kivy.lang import Builder
from kivy.core.window import Window
from dynamic_categories import generate_categories
from kivy.clock import Clock


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


class TaskManagerApp(App):
    def build(self):
        print("Inicjalizacja bazy danych...")
        initialize_database()

        self.sm = ScreenManager()

        print("Ładowanie aplikacji...")
        Builder.load_file("views.kv")

        # Dodanie ekranów do ScreenManager
        self.sm.add_widget(LoadingScreen(name='loading'))
        print("LoadingScreen załadowane.")
        self.sm.add_widget(MainMenu(name='main_menu'))
        print("MainMenu załadowane.")
        self.sm.add_widget(AddCategoryScreen(name='add_category'))
        self.sm.add_widget(DeleteCategoryScreen(name='delete_category'))
        self.sm.add_widget(CategoryListScreen(name='category_list'))
        self.sm.add_widget(TaskManagementScreen(name='task_management'))

        print("Dodane ekrany:", [screen.name for screen in self.sm.screens])

        # Ustaw ekran ładowania jako początkowy
        self.sm.current = 'loading'

        # Po opóźnieniu przejdź na główny ekran
        Clock.schedule_once(lambda dt: self.show_category_list_screen(), 2)

        return self.sm

    def show_main_menu(self):
        self.sm.current = 'main_menu'

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

        Clock.schedule_once(lambda dt: self._load_category_list(), 1)

    def _load_category_list(self):
        print("Wywołanie show_category_list_screen...")  # Debugowanie
        self.sm.current = 'category_list'
        category_list_layout = self.sm.get_screen('category_list').ids.category_list
        print("Pobrano layout kategorii:", category_list_layout)  # Debugowanie

        categories = [category[1] for category in get_categories()]
        print("Pobrane kategorie do wyświetlenia:", categories)  # Debugowanie

        generate_categories(
            category_list_layout,
            categories,
            self.manage_tasks,
            self.delete_category
        )

    def get_category_list(self):
        categories = get_categories()
        return [category[1] for category in categories]

    def add_category(self, name):
        if not name.strip():
            print("Nazwa kategorii nie może być pusta.")
            return
        try:
            self.sm.current = 'loading'
            Clock.schedule_once(lambda dt: self._add_category_logic(name), 1)
        except ValueError as e:
            print(f"Error: {e}")

    def _add_category_logic(self, name):
        add_category(name)
        print(f"Kategoria '{name}' została dodana.")
        self.show_category_list_screen()

    def delete_category(self, name):
        try:
            self.sm.current = 'loading'
            Clock.schedule_once(lambda dt: self._delete_category_logic(name), 1)
        except ValueError as e:
            print(f"Error: {e}")

    def _delete_category_logic(self, name):
        delete_category(name)
        print(f"Kategoria '{name}' została usunięta.")
        self.show_category_list_screen()

    def manage_tasks(self, category_name):
        print(f"Zarządzanie zadaniami dla kategorii: {category_name}")
        # Tutaj możesz dodać logikę przechodzenia do ekranu zarządzania zadaniami
        # np. zmiana ekranu na ekran zarządzania zadaniami


if __name__ == "__main__":
    TaskManagerApp().run()
