from pydantic import BaseModel


class SearchResult(BaseModel):
    """
    Represents a semantic search result.
    """

    chunk_id: str

    source_document: str

    page_number: int

    similarity_score: float

    text: str

    def __str__(self):
        return (
            f"SearchResult("
            f"score={self.similarity_score:.4f}, "
            f"page={self.page_number}"
            f")"
        )