from pathlib import Path
from typing import List

from pypdf import PdfReader

from app.config.settings import get_settings
from app.models.document import Document
from app.utils.logger import get_logger


logger = get_logger()
settings = get_settings()


class PDFLoader:
    """
    Loads PDF documents from the configured folder
    and converts them into Document objects.
    """

    def __init__(self):
        self.pdf_directory = Path(settings.raw_pdf_path)

    def load_documents(self) -> List[Document]:
        """
        Loads all PDF files from the raw PDF directory.

        Returns:
            List[Document]
        """

        documents: List[Document] = []

        pdf_files = sorted(self.pdf_directory.glob("*.pdf"))

        if not pdf_files:
            logger.warning(f"No PDF files found in: {self.pdf_directory}")
            return documents

        logger.info(f"Found {len(pdf_files)} PDF(s).")

        for pdf_file in pdf_files:

            try:

                logger.info(f"Reading: {pdf_file.name}")

                document = self._read_pdf(pdf_file)

                documents.append(document)

                logger.success(
                    f"Loaded '{document.file_name}' "
                    f"({document.total_pages} pages)"
                )

            except Exception as ex:

                logger.exception(
                    f"Failed to read '{pdf_file.name}'. Error: {str(ex)}"
                )

        logger.success(
            f"Successfully loaded {len(documents)} document(s)."
        )

        return documents

    def _read_pdf(self, pdf_path: Path) -> Document:
        """
        Reads a single PDF.

        Returns:
            Document
        """

        reader = PdfReader(pdf_path)

        extracted_pages = []

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                extracted_pages.append(page_text)

        full_text = "\n".join(extracted_pages)

        return Document(
            file_name=pdf_path.name,
            file_path=pdf_path,
            text=full_text,
            total_pages=len(reader.pages),
        )