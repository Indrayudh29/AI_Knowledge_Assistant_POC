from app.config.settings import get_settings
from app.utils.logger import get_logger


logger = get_logger()


def main():

    settings = get_settings()

    logger.info("=" * 60)
    logger.info("Application Started")
    logger.info(f"Application : {settings.app_name}")
    logger.info(f"Version     : {settings.app_version}")
    logger.info(f"Groq Model  : {settings.groq_model}")
    logger.info(f"Embedding   : {settings.embedding_model}")
    logger.info(f"Chunk Size  : {settings.chunk_size}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()