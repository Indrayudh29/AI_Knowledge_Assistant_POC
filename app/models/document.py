from pathlib import Path

from pydantic import BaseModel


class Document(BaseModel):
    """
    Represents a PDF document after text extraction.
    """

    file_name: str
    file_path: Path
    text: str
    total_pages: int

    def __str__(self):
        return (
            f"Document("
            f"file='{self.file_name}', "
            f"pages={self.total_pages}"
            f")"
        )