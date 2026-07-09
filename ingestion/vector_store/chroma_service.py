from typing import List

from chromadb import PersistentClient

from app.config.settings import get_settings
from app.models.chunk import Chunk
from app.models.embedding import Embedding
from app.utils.logger import get_logger


logger = get_logger()
settings = get_settings()


class ChromaService:
    """
    Service responsible for interacting with the ChromaDB vector database.

    Responsibilities
    ----------------
    - Initialize ChromaDB
    - Create or load a collection
    - Store embeddings
    - Upsert embeddings
    - Delete/reset collection

    Retrieval operations will be implemented separately.
    """

    COLLECTION_NAME = "dotnet_knowledge_base"

    def __init__(self):
        """
        Initialize the persistent ChromaDB client.
        """

        logger.info("Initializing ChromaDB...")

        self.client = PersistentClient(
            path=settings.vector_db_path
        )

        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME
        )

        logger.success(
            f"Connected to collection '{self.COLLECTION_NAME}'."
        )

    # ------------------------------------------------------------------
    # Collection Information
    # ------------------------------------------------------------------

    def get_collection_name(self) -> str:
        """
        Returns the collection name.
        """
        return self.collection.name

    def get_document_count(self) -> int:
        """
        Returns the number of stored documents.
        """
        return self.collection.count()

    def collection_exists(self) -> bool:
        """
        Checks whether the configured collection exists.
        """

        collections = self.client.list_collections()

        return any(
            collection.name == self.COLLECTION_NAME
            for collection in collections
        )

    # ------------------------------------------------------------------
    # Collection Management
    # ------------------------------------------------------------------

    def delete_collection(self) -> None:
        """
        Deletes the collection.
        """

        if not self.collection_exists():

            logger.warning(
                "Collection does not exist. Nothing to delete."
            )

            return

        logger.info(
            f"Deleting collection '{self.COLLECTION_NAME}'..."
        )

        self.client.delete_collection(
            name=self.COLLECTION_NAME
        )

        logger.success("Collection deleted.")

    def reset_collection(self) -> None:
        """
        Deletes and recreates the collection.
        """

        logger.info("Resetting ChromaDB collection...")

        if self.collection_exists():
            self.delete_collection()

        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME
        )

        logger.success(
            "Collection recreated successfully."
        )

    # ------------------------------------------------------------------
    # Embedding Storage
    # ------------------------------------------------------------------

    def add_embeddings(
        self,
        chunks: List[Chunk],
        embeddings: List[Embedding]
    ) -> None:
        """
        Adds new embeddings.

        Fails if duplicate IDs already exist.
        """

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must match."
            )

        logger.info(
            f"Adding {len(chunks)} embedding(s)..."
        )

        ids = []
        documents = []
        vectors = []
        metadatas = []

        for chunk, embedding in zip(chunks, embeddings):

            ids.append(chunk.chunk_id)
            documents.append(chunk.text)
            vectors.append(embedding.vector)
            metadatas.append(chunk.metadata)

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=vectors,
            metadatas=metadatas
        )

        logger.success(
            f"{len(ids)} embedding(s) added successfully."
        )

    def upsert_embeddings(
        self,
        chunks: List[Chunk],
        embeddings: List[Embedding]
    ) -> None:
        """
        Inserts new embeddings or updates existing ones.

        Safe to execute multiple times.
        """

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must match."
            )

        logger.info(
            f"Upserting {len(chunks)} embedding(s)..."
        )

        ids = []
        documents = []
        vectors = []
        metadatas = []

        for chunk, embedding in zip(chunks, embeddings):

            ids.append(chunk.chunk_id)
            documents.append(chunk.text)
            vectors.append(embedding.vector)
            metadatas.append(chunk.metadata)

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=vectors,
            metadatas=metadatas
        )

        logger.success(
            f"{len(ids)} embedding(s) upserted successfully."
        )