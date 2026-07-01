from pydantic import BaseModel

from app.models.chunk import Chunk


class Embedding(BaseModel):
    """
    Represents an embedding generated for a chunk.
    """

    chunk: Chunk

    vector: list[float]

    model_name: str

    dimension: int

    def __str__(self):
        return (
            f"Embedding("
            f"model='{self.model_name}', "
            f"dimension={self.dimension}"
            f")"
        )