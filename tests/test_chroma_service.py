from ingestion.loaders.pdf_loader import PDFLoader
from ingestion.cleaners.text_cleaner import TextCleaner
from ingestion.chunkers.recursive_chunker import RecursiveChunker
from ingestion.embedders.embedding_service import EmbeddingService
from ingestion.vector_store.chroma_service import ChromaService


def main():

    print("=" * 80)
    print("ChromaDB Integration Test")
    print("=" * 80)

    loader = PDFLoader()
    documents = loader.load_documents()

    cleaner = TextCleaner()
    cleaned_documents = cleaner.clean_documents(documents)

    chunker = RecursiveChunker()
    chunks = chunker.chunk_documents(cleaned_documents)

    embedding_service = EmbeddingService()
    embeddings = embedding_service.generate_embeddings(chunks)

    chroma = ChromaService()

    chroma.add_embeddings(
        chunks=chunks,
        embeddings=embeddings
    )

    print()

    print("=" * 80)

    print(
        f"Documents Stored : "
        f"{chroma.get_document_count()}"
    )

    print("=" * 80)


if __name__ == "__main__":
    main()