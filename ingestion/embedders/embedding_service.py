from typing import List

from ollama import Client

from app.config.settings import get_settings
from app.models.chunk import Chunk
from app.models.embedding import Embedding
from app.utils.logger import get_logger


logger = get_logger()
settings = get_settings()


class EmbeddingService:
    """
    Service responsible for generating vector embeddings for text chunks
    using the Ollama embedding model.

    This service converts a list of Chunk objects into a list of
    Embedding objects, which are later stored in the vector database.
    """

    def __init__(self):
        """
        Initializes the Ollama client and loads the configured
        embedding model.
        """
        self.client = Client(host=settings.ollama_host)
        self.model_name = settings.embedding_model

    def generate_embeddings(
        self,
        chunks: List[Chunk]
    ) -> List[Embedding]:
        """
        Generates embeddings for all supplied chunks.

        Args:
            chunks:
                List of Chunk objects.

        Returns:
            List[Embedding]
        """

        embeddings: List[Embedding] = []

        total_chunks = len(chunks)

        logger.info(
            f"Generating embeddings for {total_chunks} chunk(s) "
            f"using '{self.model_name}'..."
        )

        for index, chunk in enumerate(chunks, start=1):

            logger.info(
                f"[{index}/{total_chunks}] Processing '{chunk.chunk_id}'"
            )

            embedding = self._generate_embedding(chunk)

            embeddings.append(embedding)

        logger.success(
            f"Successfully generated {len(embeddings)} embedding(s)."
        )

        return embeddings

    def _generate_embedding(
        self,
        chunk: Chunk
    ) -> Embedding:
        """
        Generates an embedding for a single chunk.

        Args:
            chunk:
                Chunk object.

        Returns:
            Embedding
        """

        try:

            response = self.client.embed(
                model=self.model_name,
                input=chunk.text
            )

            if not response.embeddings:
                raise RuntimeError(
                    "Ollama returned an empty embedding response."
                )

            vector = response.embeddings[0]

            return Embedding(
                chunk_id=chunk.chunk_id,
                vector=vector,
                model_name=self.model_name,
                dimension=len(vector)
            )

        except Exception as ex:

            logger.exception(
                f"Failed to generate embedding for "
                f"'{chunk.chunk_id}'."
            )

            raise RuntimeError(
                "\nUnable to generate embedding.\n\n"
                "Please verify the following:\n"
                "1. Ollama is running.\n"
                "2. The embedding model is installed.\n"
                "3. OLLAMA_HOST is configured correctly.\n"
                "4. The input text is valid."
            ) from ex