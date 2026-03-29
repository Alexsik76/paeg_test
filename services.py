import polars as pl
import streamlit as st
from typing import List
from models import QAEntry


class DataService:
    """
    Service for loading and processing Q&A data.
    """
    
    def __init__(self, data_path: str):
        self.data_path = data_path

    @st.cache_data
    def load_data(_self) -> List[QAEntry]:
        """
        Loads the CSV data into a list of QAEntry objects using Polars.
        Cached by Streamlit to avoid reloading on every interaction.
        """
        try:
            # Using Polars for fast CSV reading
            df = pl.read_csv(_self.data_path)
            
            # Convert Polars DataFrame rows to QAEntry objects
            # Using .get() for robust column access
            return [
                QAEntry(
                    number=row.get('Number', i + 1),
                    question=row.get('Question', 'N/A'),
                    answer=row.get('Answer', 'No answer available.')
                )
                for i, row in enumerate(df.to_dicts())
            ]
        except FileNotFoundError:
            st.error(f"Error: Could not find the file {_self.data_path}.")
            return []
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return []
