import streamlit as st
from services import DataService
from config_loader import ConfigService
from ui.components import UIComponents


class AppRenderer:
    """
    Class responsible for coordinating the Streamlit application flow.
    Delegates specific UI rendering to UIComponents.
    """
    
    def __init__(self, data_service: DataService):
        self.ui = UIComponents(data_service)

    def run(self):
        """
        Main application entry point. Handles layout and global styles.
        """
        st.set_page_config(
            page_title="Система швидкого пошуку Q&A",
            page_icon="📖",
            layout="wide"
        )
        
        # Global CSS: Hide the Deploy button
        st.markdown("""
            <style>
            .stAppDeployButton {
                display: none;
            }
            </style>
            """, unsafe_allow_html=True)

        # Sidebar navigation and Help access
        with st.sidebar:
            st.title("Навігація")
            if st.button("📖 Довідка"):
                self.ui.show_help_dialog()
            st.divider()
            st.info("Використовуйте поле пошуку для знаходження відповідей.")

        # Render the main page content
        self.ui.render_search_page()


if __name__ == "__main__":
    # 1. Load configuration
    config_service = ConfigService()
    config = config_service.load()
    
    # 2. Initialize Data Service
    service = DataService(config.data_path)
    
    # 3. Create and run the application coordinator
    app = AppRenderer(service)
    app.run()
