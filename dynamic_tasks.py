from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle

TASK_HEIGHT = 60
TASK_SPACING = 10
TASK_PADDING = 5
BUTTON_WIDTH = 60
CORNER_RADIUS = [15, 15, 15, 15]

def generate_tasks(task_list_layout, tasks, edit_callback, delete_callback):
    print("Generowanie listy zadań...")
    task_list_layout.clear_widgets()

    for task in tasks:
        task_id, task_name, priority, _, _, _, category_name = task
        print(f"Generowanie zadania: {task_name} (Priorytet: {priority})")

        task_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=TASK_HEIGHT,
            spacing=TASK_SPACING
        )

        with task_box.canvas.before:
            Color(0.2, 0.4, 0.8, 1)  # Niebieski kolor
            task_box.rect = RoundedRectangle(pos=task_box.pos, size=task_box.size, radius=CORNER_RADIUS)

        task_box.bind(
            size=lambda instance, value: setattr(instance.rect, 'size', instance.size),
            pos=lambda instance, value: setattr(instance.rect, 'pos', instance.pos)
        )

        task_label = Label(
            text=f"{task_name} - Priorytet: {priority}",
            size_hint_x=0.6,
            valign="middle",
            halign="left"
        )

        def create_rounded_button(text, color, callback):
            btn = Button(
                text=text,
                size_hint_x=None,
                width=BUTTON_WIDTH,
                height=TASK_HEIGHT - TASK_PADDING,
                background_color=(0, 0, 0, 0)  # Przezroczyste tło
            )

            with btn.canvas.before:
                Color(*color)
                btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=CORNER_RADIUS)

            btn.bind(
                size=lambda instance, value: setattr(btn.rect, 'size', instance.size),
                pos=lambda instance, value: setattr(btn.rect, 'pos', instance.pos)
            )

            btn.bind(on_press=lambda instance: handle_button_press(callback, task_id, category_name))
            return btn

        def handle_button_press(callback, task_id, category_name):
            print(f"🟢 Kliknięto przycisk dla zadania ID: {task_id} (Kategoria: {category_name})")
            if callback:
                callback(task_id, category_name)
            else:
                print("🔴 BŁĄD: Nie ustawiono funkcji callback!")

        edit_button = create_rounded_button("+", (0.3, 0.7, 1, 1), edit_callback)
        delete_button = create_rounded_button("-", (0.1, 0.5, 1, 1), delete_callback)

        task_box.add_widget(task_label)
        task_box.add_widget(edit_button)
        task_box.add_widget(delete_button)

        task_list_layout.add_widget(task_box)

    print("Lista zadań wygenerowana.")

