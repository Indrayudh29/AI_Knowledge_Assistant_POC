from pydantic import BaseModel


class Chunk(BaseModel):
    """
    Represents a chunk of text generated from a document.
    """

    chunk_id: str

    source_document: str

    page_number: int

    chunk_index: int

    text: str

    def __str__(self):
        return (
            f"Chunk("
            f"id={self.chunk_id}, "
            f"page={self.page_number}, "
            f"index={self.chunk_index}"
            f")"
        )