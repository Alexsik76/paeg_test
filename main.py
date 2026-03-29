import streamlit as st
from services import DataService
from models import QAEntry


from config_loader import ConfigService


class AppRenderer:
    """
    Class responsible for rendering the Streamlit UI.
    Adheres to SRP by focusing only on user interface logic.
    """
    
    def __init__(self, data_service: DataService):
        self.data_service = data_service

    def run(self):
        """
        Main application entry point for UI logic.
        """
        st.set_page_config(page_title="Система швидкого пошуку Q&A", layout="wide")
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
            # Format: "{number}. {question}"
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
                # Use markdown to ensure LaTeX/KaTeX formulas ($...$) render correctly
                st.markdown(selected_entry.answer)


if __name__ == "__main__":
    # Load application configuration
    config_service = ConfigService()
    config = config_service.load()
    
    # Path to the data file from config
    data_path = config.data_path
    
    # Instantiate core logic services and renderer
    service = DataService(data_path)
    app = AppRenderer(service)
    
    # Start the app
    app.run()
