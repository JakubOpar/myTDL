from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle

CATEGORY_HEIGHT = 60
CATEGORY_SPACING = 10
CATEGORY_PADDING = 5
BUTTON_WIDTH = 60
CORNER_RADIUS = [15, 15, 15, 15]

def generate_categories(category_list_layout, categories, manage_callback, delete_callback):
    print("Generowanie kategorii...")
    category_list_layout.clear_widgets()

    for category_name in categories:
        print(f"Generowanie kategorii: {category_name}")

        # Główny kontener kategorii z tłem w canvas.before
        category_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=CATEGORY_HEIGHT,
            spacing=CATEGORY_SPACING
        )

        # Dodajemy tło BEZPOŚREDNIO do BoxLayout
        with category_box.canvas.before:
            Color(0.2, 0.4, 0.8, 1)  # Niebieski kolor
            category_box.rect = RoundedRectangle(pos=category_box.pos, size=category_box.size, radius=CORNER_RADIUS)

        # Wiązanie rozmiaru i pozycji tła do kontenera kategorii
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

        def create_rounded_button(text, color, callback):
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

            btn.bind(on_press=lambda instance: callback(category_name))
            return btn

        manage_button = create_rounded_button("+", (0.3, 0.7, 1, 1), manage_callback)
        delete_button = create_rounded_button("-", (0.1, 0.5, 1, 1), delete_callback)

        category_box.add_widget(category_label)
        category_box.add_widget(manage_button)
        category_box.add_widget(delete_button)

        category_list_layout.add_widget(category_box)

    print("Kategorie wygenerowane.")
