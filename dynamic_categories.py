CATEGORY_HEIGHT = 60  # Wysokość wiersza kategorii
CATEGORY_SPACING = 10  # Odstęp między elementami listy
CATEGORY_PADDING = 5  # Padding w wierszu kategorii
BUTTON_WIDTH = 60  # Szerokość przycisków

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

def generate_categories(category_list_layout, categories, manage_callback, delete_callback):
    print("Generowanie kategorii...")  # Debugowanie
    category_list_layout.clear_widgets()

    for category_name in categories:
        print(f"Generowanie kategorii: {category_name}")  # Debugowanie

        # Główny kontener kategorii
        category_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=CATEGORY_HEIGHT,
            spacing=CATEGORY_SPACING
        )

        # Dodanie tła do kategorii
        with category_box.canvas.before:
            Color(1, 0.5, 0, 1)  # Pomarańczowy kolor RGBA
            category_box.rect = Rectangle(size=category_box.size, pos=category_box.pos)
            category_box.bind(
                size=lambda instance, value: setattr(instance.rect, 'size', value),
                pos=lambda instance, value: setattr(instance.rect, 'pos', value)
            )

        # Etykieta kategorii
        category_label = Label(
            text=category_name,
            size_hint_x=0.6,
            valign="middle",
            halign="left",
            text_size=(None, None)
        )

        # Przycisk zarządzania
        manage_button = Button(
            text="+",
            size_hint_x=None,
            width=BUTTON_WIDTH,
            height=CATEGORY_HEIGHT - CATEGORY_PADDING,  # Dopasowanie wysokości do kontenera
            background_color=(0, 0.5, 1, 1),
            on_press=lambda instance, cat=category_name: manage_callback(cat)
        )

        # Przycisk usuwania
        delete_button = Button(
            text="-",
            size_hint_x=None,
            width=BUTTON_WIDTH,
            height=CATEGORY_HEIGHT - CATEGORY_PADDING,  # Dopasowanie wysokości do kontenera
            background_color=(1, 0, 0, 1),
            on_press=lambda instance, cat=category_name: delete_callback(cat)
        )

        # Dodanie elementów do kategorii
        category_box.add_widget(category_label)
        category_box.add_widget(manage_button)
        category_box.add_widget(delete_button)

        # Dodanie kategorii do listy
        category_list_layout.add_widget(category_box)

    print("Kategorie wygenerowane.")  # Debugowanie







