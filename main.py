from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from database import initialize_database, add_category, delete_category, get_categories
from kivy.lang import Builder
from kivy.core.window import Window
from dynamic_categories import generate_categories


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


class TaskManagerApp(App):
    def build(self):
        print("Inicjalizacja bazy danych...")
        initialize_database()

        self.sm = ScreenManager()

        print("Ładowanie aplikacji...")
        Builder.load_file("views.kv")

        # Dodanie ekranów do ScreenManager
        self.sm.add_widget(MainMenu(name='main_menu'))
        print("MainMenu załadowane.")
        self.sm.add_widget(AddCategoryScreen(name='add_category'))
        print("AddCategoryScreen załadowane.")
        self.sm.add_widget(DeleteCategoryScreen(name='delete_category'))
        print("DeleteCategoryScreen załadowane.")
        self.sm.add_widget(CategoryListScreen(name='category_list'))
        print("CategoryListScreen załadowane.")

        # Debugowanie: Sprawdzenie dodanych ekranów
        print("Dodane ekrany:", [screen.name for screen in self.sm.screens])

        self.sm.current = 'main_menu'  # Ustawienie ekranu początkowego

        # Automatyczne przejście na ekran kategorii po ładowaniu
        self.show_category_list_screen()

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
            add_category(name)
            print(f"Kategoria '{name}' została dodana.")
            # Powrót do listy kategorii i jej odświeżenie
            self.show_category_list_screen()
        except ValueError as e:
            print(f"Error: {e}")

    def delete_category(self, name):
        try:
            delete_category(name)
            print(f"Kategoria '{name}' została usunięta.")
            self.show_main_menu()
        except ValueError as e:
            print(f"Error: {e}")

    def manage_tasks(self, category_name):
        print(f"Zarządzanie zadaniami dla kategorii: {category_name}")
        # Tutaj możesz dodać logikę przechodzenia do ekranu zarządzania zadaniami
        # np. zmiana ekranu na ekran zarządzania zadaniami


if __name__ == "__main__":
    TaskManagerApp().run()
