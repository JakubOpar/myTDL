from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle

CATEGORY_HEIGHT = 60
CATEGORY_SPACING = 10
CATEGORY_PADDING = 5
BUTTON_WIDTH = 60
CORNER_RADIUS = [15, 15, 15, 15]


def generate_categories(category_list_layout, categories, task_callback, delete_callback):
    """Generuje dynamiczną listę kategorii."""

    print("🛠 Generowanie kategorii...")
    category_list_layout.clear_widgets()

    for category_name in categories:
        print(f"🎯 Generowanie kategorii: {category_name}")

        category_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=CATEGORY_HEIGHT,
            spacing=CATEGORY_SPACING
        )

        with category_box.canvas.before:
            Color(0.2, 0.4, 0.8, 1)  # Niebieski kolor
            category_box.rect = RoundedRectangle(pos=category_box.pos, size=category_box.size, radius=CORNER_RADIUS)

        category_box.bind(
            size=lambda instance, value: setattr(instance.rect, 'size', instance.size),
            pos=lambda instance, value: setattr(instance.rect, 'pos', instance.pos)
        )

        category_label = Label(
            text=category_name,
            size_hint_x=0.6,
            valign="middle",
            halign="left"
        )

        def create_rounded_button(text, color, callback, cat_name):
            """Tworzy zaokrąglony przycisk z poprawnym przekazywaniem kategorii."""
            btn = Button(
                text=text,
                size_hint_x=None,
                width=BUTTON_WIDTH,
                height=CATEGORY_HEIGHT - CATEGORY_PADDING,
                background_color=(0, 0, 0, 0)  # Przezroczyste tło
            )

            with btn.canvas.before:
                Color(*color)
                btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=CORNER_RADIUS)

            btn.bind(
                size=lambda instance, value: setattr(btn.rect, 'size', instance.size),
                pos=lambda instance, value: setattr(btn.rect, 'pos', instance.pos)
            )

            # Poprawne przekazywanie wartości kategorii do callbacka
            btn.bind(on_release=lambda instance: handle_button_press(callback, cat_name))
            return btn

        def handle_button_press(callback, cat_name):
            """Obsługuje naciśnięcie przycisku, logując i wywołując przekazaną funkcję."""
            print(f"🟢 Kliknięto przycisk w kategorii: {cat_name}")
            if callback:
                callback(cat_name)
            else:
                print("🔴 BŁĄD: Nie ustawiono funkcji callback!")

        # Tworzymy przyciski z poprawnym przekazywaniem kategorii
        task_button = create_rounded_button("+", (0.3, 0.7, 1, 1), task_callback, category_name)
        delete_button = create_rounded_button("-", (0.1, 0.5, 1, 1), delete_callback, category_name)

        # Dodajemy elementy do kontenera
        category_box.add_widget(category_label)
        category_box.add_widget(task_button)
        category_box.add_widget(delete_button)

        # Dodajemy kontener kategorii do layoutu
        category_list_layout.add_widget(category_box)

    print("✅ Kategorie wygenerowane.")
