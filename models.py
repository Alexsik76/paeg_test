from dataclasses import dataclass


@dataclass
class QAEntry:
    """
    Data model for a Question-Answer pair.
    """
    number: int
    question: str
    answer: str
