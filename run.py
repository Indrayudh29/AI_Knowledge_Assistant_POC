from app.config.settings import get_settings


def main():

    settings = get_settings()

    print("=" * 50)

    print(settings.app_name)

    print("Version :", settings.app_version)

    print("Model   :", settings.groq_model)

    print("Embedding :", settings.embedding_model)

    print("Chunk Size :", settings.chunk_size)

    print("=" * 50)


if __name__ == "__main__":
    main()