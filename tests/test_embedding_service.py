from ingestion.loaders.pdf_loader import PDFLoader
from ingestion.cleaners.text_cleaner import TextCleaner
from ingestion.chunkers.recursive_chunker import RecursiveChunker
from ingestion.embedders.embedding_service import EmbeddingService


def main():

    print("=" * 80)
    print("Embedding Service Test")
    print("=" * 80)

    loader = PDFLoader()
    documents = loader.load_documents()

    cleaner = TextCleaner()
    cleaned_documents = cleaner.clean_documents(documents)

    chunker = RecursiveChunker()
    chunks = chunker.chunk_documents(cleaned_documents)

    service = EmbeddingService()

    embeddings = service.generate_embeddings(chunks)

    print()

    print("=" * 80)
    print(f"Generated Embeddings : {len(embeddings)}")
    print("=" * 80)

    first = embeddings[0]

    print()

    print(first)

    print()

    print(f"Vector Dimension : {first.dimension}")

    print()

    print("First 10 values:")

    print(first.vector[:10])


if __name__ == "__main__":
    main()