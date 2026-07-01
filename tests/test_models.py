from pathlib import Path

from app.models.document import Document
from app.models.chunk import Chunk
from app.models.embedding import Embedding
from app.models.search_result import SearchResult


def main():

    document = Document(
        file_name="dependency_injection.pdf",
        file_path=Path("knowledge/raw_pdfs/dependency_injection.pdf"),
        text="Sample document text.",
        total_pages=25
    )

    print(document)

    chunk = Chunk(
        chunk_id="chunk_001",
        source_document=document.file_name,
        page_number=1,
        chunk_index=1,
        text="Dependency Injection allows..."
    )

    print(chunk)

    embedding = Embedding(
        chunk=chunk,
        vector=[0.12, 0.87, 0.44],
        model_name="nomic-embed-text",
        dimension=3
    )

    print(embedding)

    result = SearchResult(
        chunk_id="chunk_001",
        source_document=document.file_name,
        page_number=1,
        similarity_score=0.95,
        text="Dependency Injection allows..."
    )

    print(result)


if __name__ == "__main__":
    main()