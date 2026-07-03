from ingestion.cleaners.text_cleaner import TextCleaner
from ingestion.chunkers.recursive_chunker import RecursiveChunker
from ingestion.loaders.pdf_loader import PDFLoader


def main():

    print()

    print("=" * 70)

    print("Recursive Chunking Test")

    print("=" * 70)

    loader = PDFLoader()

    documents = loader.load_documents()

    cleaner = TextCleaner()

    cleaned_documents = cleaner.clean_documents(documents)

    chunker = RecursiveChunker()

    chunks = chunker.chunk_documents(cleaned_documents)

    print()

    print("=" * 70)

    print(f"Total Chunks Generated : {len(chunks)}")

    print("=" * 70)

    print()

    for chunk in chunks[:5]:

        print(chunk)

        print(chunk.metadata)

        print()

        print(chunk.text[:200])

        print()

        print("-" * 70)


if __name__ == "__main__":
    main()