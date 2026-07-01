from pathlib import Path

from app.utils.logger import get_logger

logger = get_logger()


class ProjectValidator:
    """
    Validates the project structure before execution.
    """

    REQUIRED_PATHS = [
        "knowledge/raw_pdfs",
        "knowledge/processed_texts",
        "knowledge/chunks",
        "knowledge/metadata",
        "chroma_db",
        "logs",
        "reports",
        "prompts",
        "tests",
        "scripts"
    ]

    REQUIRED_FILES = [
        ".env",
        "requirements.txt"
    ]

    @classmethod
    def validate(cls) -> bool:

        logger.info("Starting project validation...")

        validation_passed = True

        # -------------------------------
        # Check required files
        # -------------------------------

        for file in cls.REQUIRED_FILES:

            if Path(file).exists():
                logger.success(f"Found file: {file}")
            else:
                logger.error(f"Missing file: {file}")
                validation_passed = False

        # -------------------------------
        # Check required directories
        # -------------------------------

        for folder in cls.REQUIRED_PATHS:

            if Path(folder).exists():
                logger.success(f"Found folder: {folder}")
            else:
                logger.error(f"Missing folder: {folder}")
                validation_passed = False

        # -------------------------------

        if validation_passed:
            logger.success("Project validation completed successfully.")
        else:
            logger.error("Project validation failed.")

        return validation_passed