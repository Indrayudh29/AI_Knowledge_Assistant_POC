from app.config.settings import get_settings
from app.utils.logger import get_logger
from scripts.project_validator import ProjectValidator

logger = get_logger()


def print_banner(settings):
    """
    Prints application information.
    """

    logger.info("=" * 60)
    logger.info(settings.app_name)
    logger.info(f"Version           : {settings.app_version}")
    logger.info(f"Groq Model        : {settings.groq_model}")
    logger.info(f"Embedding Model   : {settings.embedding_model}")
    logger.info(f"Chunk Size        : {settings.chunk_size}")
    logger.info(f"Chunk Overlap     : {settings.chunk_overlap}")
    logger.info("=" * 60)


def main():

    settings = get_settings()

    print_banner(settings)

    if not ProjectValidator.validate():
        logger.error("Application startup aborted.")
        return

    logger.success("Application started successfully.")
    logger.info("Ready for pipeline execution.")


if __name__ == "__main__":
    main()