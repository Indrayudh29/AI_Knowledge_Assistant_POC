import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.settings import get_settings
from app.models.chunk import Chunk
from app.models.document import Document
from app.utils.logger import get_logger


logger = get_logger()
settings = get_settings()


class RecursiveChunker:
    """
    Splits cleaned documents into overlapping chunks using
    LangChain's RecursiveCharacterTextSplitter.

    Each document generates:
        - List[Chunk]
        - JSON file under knowledge/chunks
    """

    def __init__(self):

        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap

        self.output_folder = Path(settings.chunk_path)

        self.output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=self.chunk_size,

            chunk_overlap=self.chunk_overlap,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def chunk_documents(
        self,
        documents: list[Document]
    ) -> list[Chunk]:

        """
        Splits all documents into chunks.

        Returns:
            List[Chunk]
        """

        all_chunks = []

        logger.info(
            f"Starting chunk generation for {len(documents)} document(s)."
        )

        for document in documents:

            chunks = self._chunk_single_document(document)

            all_chunks.extend(chunks)

        logger.success(
            f"Generated {len(all_chunks)} chunk(s)."
        )

        return all_chunks

    def _chunk_single_document(
        self,
        document: Document
    ) -> list[Chunk]:

        logger.info(
            f"Chunking '{document.file_name}'..."
        )

        text_chunks = self.splitter.split_text(document.text)

        document_chunks = []

        document_name = Path(document.file_name).stem

        for index, text in enumerate(text_chunks, start=1):

            chunk_id = f"{document_name}_{index:04d}"

            metadata = {
               "source_document": document.file_name,
                "chunk_index": index,
                "character_count": len(text)
            }

            chunk = Chunk(

                chunk_id=chunk_id,

                source_document=document.file_name,

                chunk_index=index,

                text=text,

                metadata=metadata

            )

            document_chunks.append(chunk)

        self._save_chunks(
            document_name,
            document_chunks
        )

        logger.success(
            f"{document.file_name} -> {len(document_chunks)} chunks"
        )

        return document_chunks

    def _save_chunks(
        self,
        document_name: str,
        chunks: list[Chunk]
    ):

        output_file = (
            self.output_folder /
            f"{document_name}_chunks.json"
        )

        json_data = [
            chunk.model_dump()
            for chunk in chunks
        ]

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                json_data,
                file,
                indent=4,
                ensure_ascii=False
            )

        logger.info(
            f"Saved {len(chunks)} chunk(s) -> {output_file.name}"
        )