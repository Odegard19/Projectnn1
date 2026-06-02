import customtkinter as ctk
import json
import os
import uuid

# ==========================================
# КОНФИГУРАЦИЯ И НАСТРОЙКИ
# ==========================================
DATA_FILE = "tasks.json"

class SmartTaskManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- НАСТРОЙКА ОКНА ---
        self.title("Smart Task Manager")
        self.geometry("750x850")
        self.minsize(600, 700)
        
        # Дизайн: Темная тема по умолчанию, синие акценты (кнопки)
        ctk.set_appearance_mode("dark")  
        ctk.set_default_color_theme("blue")  

        # --- ДАННЫЕ ---
        # Загружаем задачи при старте приложения
        self.tasks = self.load_tasks()

        # --- ИНИЦИАЛИЗАЦИЯ ИНТЕРФЕЙСА ---
        self.create_widgets()
        self.render_tasks()

    # ==========================================
    # ЛОГИКА РАБОТЫ С ДАННЫМИ (Хранение JSON)
    # ==========================================
    def load_tasks(self):
        """Загрузка задач из JSON-файла. Возвращает пустой список, если файла нет."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return [] # Если файл поврежден, возвращаем пустой список
        return []

    def save_tasks(self):
        """Сохранение задач в JSON-файл."""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    # ==========================================
    # ЛОГИКА БИЗНЕС-ПРОЦЕССОВ
    # ==========================================
    def calculate_priority(self, urgency, importance):
        """
        Вычисление индекса приоритета (P).
        Формула: P = (Срочность * 0.6) + (Важность * 0.4)
        """
        return (urgency * 0.6) + (importance * 0.4)

    def add_task(self):
        """Считывание данных из полей и добавление новой задачи в список."""
        name = self.name_entry.get().strip()
        desc = self.desc_entry.get().strip()
        urgency = int(self.urgency_slider.get())
        importance = int(self.importance_slider.get())

        # Проверка: название задачи обязательно
        if not name:
            self.name_entry.configure(placeholder_text_color="red") # Подсказка об ошибке
            return

        self.name_entry.configure(placeholder_text_color="gray")

        # Рассчитываем приоритет
        priority = self.calculate_priority(urgency, importance)

        # Создаем словарь задачи (uuid нужен для уникального ID)
        new_task = {
            "id": str(uuid.uuid4()),
            "name": name,
            "desc": desc,
            "urgency": urgency,
            "importance": importance,
            "priority": round(priority, 2), # Округляем для красоты
            "done": False
        }

        # Добавляем, сохраняем и обновляем экран
        self.tasks.append(new_task)
        self.save_tasks()
        
        # Сброс полей к значениям по умолчанию
        self.name_entry.delete(0, 'end')
        self.desc_entry.delete(0, 'end')
        self.urgency_slider.set(5)
        self.update_urgency_label(5)
        self.importance_slider.set(5)
        self.update_importance_label(5)

        self.render_tasks()

    def smart_sort(self):
        """Сортировка задач по индексу приоритета (P) по убыванию."""
        # Ключ сортировки — priority (сначала самые приоритетные)
        self.tasks.sort(key=lambda x: x['priority'], reverse=True)
        self.save_tasks()
        self.render_tasks()

    def toggle_done(self, task_id):
        """Отметить задачу как выполненную / невыполненную."""
        for task in self.tasks:
            if task['id'] == task_id:
                task['done'] = not task['done']
                break
        self.save_tasks()
        self.render_tasks()

    def delete_task(self, task_id):
        """Удаление задачи из списка (доп. функция для удобства)."""
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.save_tasks()
        self.render_tasks()

    # ==========================================
    # ИНТЕРФЕЙС И ГРАФИКА
    # ==========================================
    def update_urgency_label(self, value):
        """Обновляет текст ярлыка при движении слайдера срочности."""
        self.urgency_label.configure(text=f"Срочность: {int(value)}")

    def update_importance_label(self, value):
        """Обновляет текст ярлыка при движении слайдера важности."""
        self.importance_label.configure(text=f"Важность: {int(value)}")

    def create_widgets(self):
        """Создание статических элементов окна (форма добавления, кнопки)."""
        # --- Заголовок ---
        self.title_label = ctk.CTkLabel(self, text="Smart Task Manager", font=ctk.CTkFont(size=28, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        # --- Форма добавления задачи (Фрейм) ---
        self.input_frame = ctk.CTkFrame(self, corner_radius=15)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        # Поля ввода
        self.name_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Название задачи...", height=40, font=ctk.CTkFont(size=14))
        self.name_entry.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew", columnspan=2)

        self.desc_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Описание задачи (опционально)...", height=40, font=ctk.CTkFont(size=14))
        self.desc_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew", columnspan=2)

        # Ползунки (Sliders) Срочности и Важности
        self.urgency_label = ctk.CTkLabel(self.input_frame, text="Срочность: 5", font=ctk.CTkFont(weight="bold"))
        self.urgency_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.urgency_slider = ctk.CTkSlider(self.input_frame, from_=1, to=10, number_of_steps=9, command=self.update_urgency_label)
        self.urgency_slider.set(5)
        self.urgency_slider.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="ew")

        self.importance_label = ctk.CTkLabel(self.input_frame, text="Важность: 5", font=ctk.CTkFont(weight="bold"))
        self.importance_label.grid(row=2, column=1, padx=20, pady=(10, 0), sticky="w")
        
        self.importance_slider = ctk.CTkSlider(self.input_frame, from_=1, to=10, number_of_steps=9, command=self.update_importance_label)
        self.importance_slider.set(5)
        self.importance_slider.grid(row=3, column=1, padx=20, pady=(5, 10), sticky="ew")

        # Кнопка "Добавить"
        self.add_button = ctk.CTkButton(self.input_frame, text="Добавить задачу", height=40, font=ctk.CTkFont(weight="bold"), command=self.add_task)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=(10, 20))

        # Выравнивание колонок
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=1)

        # --- Кнопка "Умная сортировка" ---
        self.sort_button = ctk.CTkButton(
            self, 
            text="✨ Умная сортировка (по приоритету)", 
            fg_color="#D35400", # Оранжевый цвет для кнопки сортировки
            hover_color="#E67E22", 
            height=40,
            font=ctk.CTkFont(weight="bold", size=14),
            command=self.smart_sort
        )
        self.sort_button.pack(pady=15, padx=20, fill="x")

        # --- Скроллируемый список задач ---
        self.tasks_scrollable_frame = ctk.CTkScrollableFrame(self, corner_radius=15, fg_color="transparent")
        self.tasks_scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

    def render_tasks(self):
        """Отрисовка всех задач в скроллируемом списке."""
        # Удаляем старые виджеты перед перерисовкой
        for widget in self.tasks_scrollable_frame.winfo_children():
            widget.destroy()

        for task in self.tasks:
            # 1. Выбираем цвет фона в зависимости от приоритета (Темная тема)
            # Высокий (>= 7.5) -> Бордовый, Средний (>= 5.0) -> Горчичный/Оранжевый, Низкий -> Темно-зеленый
            if task['done']:
                frame_color = "#303030" # Темно-серый, если выполнено
            elif task['priority'] >= 7.5:
                frame_color = "#5C2020" # Красный (High Priority)
            elif task['priority'] >= 5.0:
                frame_color = "#6B5000" # Желтый/Оранжевый (Medium Priority)
            else:
                frame_color = "#1B4D2B" # Зеленый (Low Priority)

            # Фрейм отдельной задачи
            task_frame = ctk.CTkFrame(self.tasks_scrollable_frame, fg_color=frame_color, corner_radius=10)
            task_frame.pack(fill="x", pady=8, padx=5)

            # 2. Checkbox выполнения (Чекбокс)
            checkbox_var = ctk.BooleanVar(value=task['done'])
            checkbox = ctk.CTkCheckBox(
                task_frame, 
                text="", 
                variable=checkbox_var, 
                command=lambda t_id=task['id']: self.toggle_done(t_id),
                width=20,
                corner_radius=5
            )
            checkbox.pack(side="left", padx=15, pady=15)

            # 3. Текстовая информация (Фрейм)
            info_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=5, pady=10)

            # Название: если выполнено, зачеркиваем (имитация через серый цвет текста)
            text_color = "gray" if task['done'] else "white"
            name_font = ctk.CTkFont(size=16, weight="bold", overstrike=task['done'])
            
            name_label = ctk.CTkLabel(info_frame, text=task['name'], font=name_font, text_color=text_color)
            name_label.pack(anchor="w")

            # Описание
            if task['desc']:
                desc_label = ctk.CTkLabel(info_frame, text=task['desc'], font=ctk.CTkFont(size=13), text_color=text_color)
                desc_label.pack(anchor="w")

            # Мета-данные (Приоритет)
            meta_text = f"⚡ Срочность: {task['urgency']}  |  📌 Важность: {task['importance']}  |  🔥 Приоритет (P): {task['priority']}"
            meta_label = ctk.CTkLabel(info_frame, text=meta_text, font=ctk.CTkFont(size=11, slant="italic"), text_color="#A0A0A0")
            meta_label.pack(anchor="w", pady=(5, 0))

            # 4. Кнопка удаления (Х)
            delete_btn = ctk.CTkButton(
                task_frame, 
                text="X", 
                width=30, 
                height=30, 
                fg_color="transparent", 
                hover_color="#FF4C4C",
                text_color="white",
                command=lambda t_id=task['id']: self.delete_task(t_id)
            )
            delete_btn.pack(side="right", padx=15)

# ==========================================
# ТОЧКА ВХОДА (Запуск приложения)
# ==========================================
if __name__ == "__main__":
    app = SmartTaskManager()
    app.mainloop()
