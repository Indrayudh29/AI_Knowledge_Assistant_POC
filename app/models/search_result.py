from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    """
    Represents a semantic search result returned from the vector database.
    """

    chunk_id: str

    source_document: str

    similarity_score: float

    text: str

    metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)

    def __str__(self):
        return (
            f"SearchResult("
            f"score={self.similarity_score:.4f}, "
            f"document='{self.source_document}'"
            f")"
        )