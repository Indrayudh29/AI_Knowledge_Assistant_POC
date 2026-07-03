from pathlib import Path

from app.models.document import Document
from app.models.chunk import Chunk
from app.models.embedding import Embedding
from app.models.search_result import SearchResult


def main():

    print("=" * 70)
    print("Testing Domain Models")
    print("=" * 70)

    # ---------------------------------------------------------
    # Document
    # ---------------------------------------------------------

    document = Document(
        file_name="dependency_injection.pdf",
        file_path=Path("knowledge/raw_pdfs/dependency_injection.pdf"),
        text="Sample document text.",
        total_pages=25,
    )

    print(document)

    # ---------------------------------------------------------
    # Chunk
    # ---------------------------------------------------------

    chunk = Chunk(
        chunk_id="chunk_001",
        source_document=document.file_name,
        chunk_index=1,
        text="Dependency Injection allows classes to receive their dependencies.",
        metadata={
            "source": document.file_name,
            "chunk_index": 1,
            "characters": 67
        }
    )

    print(chunk)

    # ---------------------------------------------------------
    # Embedding
    # ---------------------------------------------------------

    embedding = Embedding(
        chunk=chunk,
        vector=[0.12, 0.87, 0.44],
        model_name="nomic-embed-text",
        dimension=3,
    )

    print(embedding)

    # ---------------------------------------------------------
    # Search Result
    # ---------------------------------------------------------

    result = SearchResult(
        chunk_id=chunk.chunk_id,
        source_document=document.file_name,
        similarity_score=0.95,
        text=chunk.text,
        metadata=chunk.metadata
    )

    print(result)

    print("=" * 70)
    print("All domain model tests completed successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()