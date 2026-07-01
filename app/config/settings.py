from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central configuration class.

    Loads all values from the .env file.

    This class should be the ONLY place where environment
    variables are read.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    # --------------------------------------------------
    # Application
    # --------------------------------------------------

    app_name: str = Field(alias="APP_NAME")
    app_version: str = Field(alias="APP_VERSION")
    log_level: str = Field(alias="LOG_LEVEL")

    # --------------------------------------------------
    # Groq
    # --------------------------------------------------

    groq_api_key: str = Field(alias="GROQ_API_KEY")
    groq_model: str = Field(alias="GROQ_MODEL")

    # --------------------------------------------------
    # Embeddings
    # --------------------------------------------------

    embedding_provider: str = Field(alias="EMBEDDING_PROVIDER")
    embedding_model: str = Field(alias="EMBEDDING_MODEL")

    # --------------------------------------------------
    # Chunking
    # --------------------------------------------------

    chunk_size: int = Field(alias="CHUNK_SIZE")
    chunk_overlap: int = Field(alias="CHUNK_OVERLAP")

    # --------------------------------------------------
    # Paths
    # --------------------------------------------------

    raw_pdf_path: str = Field(alias="RAW_PDF_PATH")
    processed_text_path: str = Field(alias="PROCESSED_TEXT_PATH")
    chunk_path: str = Field(alias="CHUNK_PATH")
    metadata_path: str = Field(alias="METADATA_PATH")
    vector_db_path: str = Field(alias="VECTOR_DB_PATH")

    # --------------------------------------------------
    # Retrieval
    # --------------------------------------------------

    top_k_results: int = Field(alias="TOP_K_RESULTS")


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings object.

    The configuration is loaded only once.
    """
    return Settings()