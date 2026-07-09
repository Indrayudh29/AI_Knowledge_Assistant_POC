import time

from ingestion.loaders.pdf_loader import PDFLoader
from ingestion.cleaners.text_cleaner import TextCleaner
from ingestion.chunkers.recursive_chunker import RecursiveChunker
from ingestion.embedders.embedding_service import EmbeddingService
from ingestion.vector_store.chroma_service import ChromaService

from app.utils.logger import get_logger


logger = get_logger()


class IngestionPipeline:
    """
    Orchestrates the complete document ingestion pipeline.

    Pipeline Flow
    -------------
    PDFs
        ↓
    PDF Loader
        ↓
    Text Cleaner
        ↓
    Recursive Chunker
        ↓
    Embedding Service
        ↓
    ChromaDB
    """

    def __init__(self):

        self.loader = PDFLoader()

        self.cleaner = TextCleaner()

        self.chunker = RecursiveChunker()

        self.embedding_service = EmbeddingService()

        self.vector_store = ChromaService()

    def run(
        self,
        reset_database: bool = True
    ) -> None:
        """
        Executes the complete ingestion pipeline.
        """

        start_time = time.time()

        logger.info("=" * 80)
        logger.info("Starting AI Knowledge Assistant Ingestion Pipeline")
        logger.info("=" * 80)

        # --------------------------------------------------
        # Step 1 : Load PDFs
        # --------------------------------------------------

        documents = self.loader.load_documents()

        # --------------------------------------------------
        # Step 2 : Clean Text
        # --------------------------------------------------

        cleaned_documents = self.cleaner.clean_documents(
            documents
        )

        # --------------------------------------------------
        # Step 3 : Generate Chunks
        # --------------------------------------------------

        chunks = self.chunker.chunk_documents(
            cleaned_documents
        )

        # --------------------------------------------------
        # Step 4 : Generate Embeddings
        # --------------------------------------------------

        embeddings = self.embedding_service.generate_embeddings(
            chunks
        )

        # --------------------------------------------------
        # Step 5 : Reset Chroma (Development)
        # --------------------------------------------------

        if reset_database:

            logger.info("Resetting ChromaDB...")

            self.vector_store.reset_collection()

        # --------------------------------------------------
        # Step 6 : Store Embeddings
        # --------------------------------------------------

        self.vector_store.upsert_embeddings(
            chunks,
            embeddings
        )

        elapsed = time.time() - start_time

        logger.info("=" * 80)
        logger.success("Pipeline completed successfully.")
        logger.info("=" * 80)

        logger.info(f"Documents Processed : {len(documents)}")
        logger.info(f"Chunks Generated    : {len(chunks)}")
        logger.info(f"Embeddings Created  : {len(embeddings)}")
        logger.info(
            f"Vectors Stored      : "
            f"{self.vector_store.get_document_count()}"
        )
        logger.info(f"Elapsed Time        : {elapsed:.2f} seconds")

        logger.info("=" * 80)


def main():

    pipeline = IngestionPipeline()

    pipeline.run(
        reset_database=True
    )


if __name__ == "__main__":
    main()