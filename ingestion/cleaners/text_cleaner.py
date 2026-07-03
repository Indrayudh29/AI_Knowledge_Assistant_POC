import re
from pathlib import Path

from app.config.settings import get_settings
from app.models.document import Document
from app.utils.logger import get_logger

logger = get_logger()
settings = get_settings()


class TextCleaner:
    """
    Cleans extracted PDF text and saves it
    to the processed_text folder.
    """

    def __init__(self):

        self.output_folder = Path(settings.processed_text_path)

        self.output_folder.mkdir(parents=True, exist_ok=True)

    def clean_document(self, document: Document) -> Document:
        """
        Cleans a document and returns a new Document.
        """

        logger.info(f"Cleaning '{document.file_name}'")

        cleaned_text = self._clean_text(document.text)

        output_file = self.output_folder / (
            Path(document.file_name).stem + ".txt"
        )

        output_file.write_text(
            cleaned_text,
            encoding="utf-8"
        )

        logger.success(f"Saved cleaned text -> {output_file.name}")

        return Document(
            file_name=document.file_name,
            file_path=document.file_path,
            text=cleaned_text,
            total_pages=document.total_pages
        )

    def clean_documents(
        self,
        documents: list[Document]
    ) -> list[Document]:

        cleaned_documents = []

        for document in documents:

            cleaned_documents.append(
                self.clean_document(document)
            )

        logger.success(
            f"Cleaned {len(cleaned_documents)} document(s)."
        )

        return cleaned_documents

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Performs generic text cleaning.
        """

        # Windows -> Unix line endings
        text = text.replace("\r\n", "\n")

        # Remove tabs
        text = text.replace("\t", " ")

        # Collapse multiple spaces
        text = re.sub(r"[ ]{2,}", " ", text)

        # Collapse excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove trailing spaces
        text = "\n".join(
            line.strip()
            for line in text.splitlines()
        )

        return text.strip()