from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from database import initialize_database, add_category, delete_category, get_categories
from kivy.lang import Builder


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

    def show_category_list_screen(self):
        self.sm.current = 'category_list'

    def get_category_list(self):
        return [category[1] for category in get_categories()]

    def add_category(self, name):
        try:
            add_category(name)
            self.show_main_menu()
        except ValueError as e:
            print(e)

    def delete_category(self, name):
        try:
            delete_category(name)
            self.show_main_menu()
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    TaskManagerApp().run()
