from ingestion.loaders.pdf_loader import PDFLoader
from ingestion.cleaners.text_cleaner import TextCleaner


def main():

    loader = PDFLoader()

    documents = loader.load_documents()

    cleaner = TextCleaner()

    cleaned_documents = cleaner.clean_documents(documents)

    print()

    print("=" * 60)

    print("Cleaning Summary")

    print("=" * 60)

    for document in cleaned_documents:

        print(document.file_name)

        print(f"Characters : {len(document.text):,}")

        print("-" * 60)


if __name__ == "__main__":
    main()