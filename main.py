from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from database import initialize_database, add_category, delete_category, get_categories
from kivy.lang import Builder
from kivy.uix.label import Label


class MainMenu(Screen):
    pass


class AddCategoryScreen(Screen):
    pass


class DeleteCategoryScreen(Screen):
    pass


class CategoryListScreen(Screen):
    pass


class TaskManagerApp(App):
    def build(self):
        initialize_database()
        self.sm = ScreenManager()
        print("Ładowanie aplikacji...")

        print("Ładowanie pliku views.kv...")
        Builder.load_file("views.kv")

        self.sm.add_widget(MainMenu(name='main_menu'))
        print("MainMenu załadowane.")
        self.sm.add_widget(AddCategoryScreen(name='add_category'))
        self.sm.add_widget(DeleteCategoryScreen(name='delete_category'))
        self.sm.add_widget(CategoryListScreen(name='category_list'))

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
        self.sm.current = 'category_list'
        category_list_layout = self.sm.get_screen('category_list').ids.category_list

        category_list_layout.clear_widgets()

        categories = self.get_category_list()
        if categories:
            for category in categories:
                category_label = Label(text=category, size_hint_y=None, height=40)
                category_list_layout.add_widget(category_label)
        else:
            category_list_layout.add_widget(Label(text="Brak kategorii"))

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
            self.show_main_menu()
        except ValueError as e:
            print(f"Error: {e}")

    def delete_category(self, name):
        try:
            delete_category(name)
            print(f"Kategoria '{name}' została usunięta.")
            self.show_main_menu()
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    TaskManagerApp().run()
