from pydantic import BaseModel

from app.models.chunk import Chunk


class Embedding(BaseModel):
    """
    Represents an embedding generated for a text chunk.

    This object is created after the embedding model converts
    a Chunk into a numerical vector. It is later stored in the
    vector database along with the chunk metadata.
    """

    chunk: Chunk

    vector: list[float]

    model_name: str

    dimension: int

    def __str__(self):
        return (
            f"Embedding("
            f"model='{self.model_name}', "
            f"dimension={self.dimension}, "
            f"chunk_id='{self.chunk.chunk_id}'"
            f")"
        )