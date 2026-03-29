import streamlit as st
from services import DataService


class UIComponents:
    """
    Component-based UI logic for the Streamlit application.
    Encapsulates specific page rendering and interactive dialogs.
    """
    
    def __init__(self, data_service: DataService):
        self.data_service = data_service

    @st.dialog("Довідка та документація")
    def show_help_dialog(self):
        """
        Displays help information in a modal dialog.
        """
        st.markdown("""
        ### 🔗 Репозиторій проекту
        Вихідний код доступний за адресою: [https://github.com/Alexsik76/paeg_test](https://github.com/Alexsik76/paeg_test)

        ### 🚀 Локальний запуск
        1. **Створіть venv**: `python -m venv venv`
        2. **Активуйте venv**:
           - Windows: `.\\venv\\Scripts\\activate`
           - Linux/macOS: `source venv/bin/activate`
        3. **Встановіть залежності**: `pip install -r requirements.txt`
        4. **Запустіть додаток**: `streamlit run main.py`

        ### 📊 Як оновити базу питань (data/test.csv) (Лише для локального запуску)
        1. Відкрийте файл `data/test.csv` у **Microsoft Excel**.
        2. Для коректних символів: **Дані -> З тексту/CSV** (оберіть UTF-8).
        3. Внесіть зміни у колонки `Number`, `Question` або `Answer`.
        4. Збережіть як **CSV (UTF-8)**.
        5. Замініть файл у папці `data`. Додаток оновить дані автоматично.
        """)

    def render_search_page(self):
        """
        Renders the main Q&A search interface.
        """
        st.title("Система швидкого пошуку Q&A")

        # Load cached data via DataService
        qa_data = self.data_service.load_data()
        
        if not qa_data:
            st.warning("Дані не знайдено. Перевірте джерело даних або конфігурацію.")
            return

        # List of questions with numbers for better selection
        questions_display = [f"{entry.number}. {entry.question}" for entry in qa_data]
        
        # Interaction with selectbox in Ukrainian
        selected_question_text = st.selectbox(
            "Введіть текст для фільтрації та оберіть питання:",
            options=questions_display,
            index=None,
            placeholder="Почніть писати для пошуку..."
        )

        if selected_question_text:
            # Find the answer by extracting the number from the selected text
            try:
                selected_num = int(selected_question_text.split('.')[0])
                selected_entry = next(
                    (entry for entry in qa_data if entry.number == selected_num),
                    None
                )
            except (ValueError, IndexError):
                selected_entry = None
            
            if selected_entry:
                st.markdown("---")
                st.markdown("### Відповідь:")
                st.markdown(selected_entry.answer)
