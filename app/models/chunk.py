from pydantic import BaseModel, Field


class Chunk(BaseModel):
    """
    Represents a chunk of text generated from a document.

    This object is created after chunking a document and is later
    converted into an embedding before being stored in the vector database.
    """

    chunk_id: str

    source_document: str

    chunk_index: int

    text: str

    metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)

    def __str__(self):
        return (
            f"Chunk("
            f"id='{self.chunk_id}', "
            f"document='{self.source_document}', "
            f"index={self.chunk_index}"
            f")"
        )