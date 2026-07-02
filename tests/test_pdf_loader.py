from ingestion.loaders.pdf_loader import PDFLoader


def main():

    loader = PDFLoader()

    documents = loader.load_documents()

    print()

    print("=" * 60)

    print(f"Total Documents Loaded : {len(documents)}")

    print("=" * 60)

    for document in documents:

        print(document)

        print(f"Characters : {len(document.text):,}")

        print("-" * 60)


if __name__ == "__main__":
    main()