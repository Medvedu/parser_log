import argparse

from src.services.application import Application


def main():
    parser = argparse.ArgumentParser(description="Парсер логов сервера")
    parser.add_argument(
        "--config",
        type=str,
        help="Путь до config файла",
        nargs="?",
    )

    args = parser.parse_args()
    application = Application(args)
    application.run()


if __name__ == "__main__":
    main()
