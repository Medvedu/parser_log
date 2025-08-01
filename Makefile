# Формально требуется запускать скрипт через Makefile, тем не менее рекомендуемый
# способ описан в README.md.
#
# Запуск с заданным файлом конфигурации через Makefile:
# ```shell
# $ make run_script config='path/to/file'
# ```
#
run_script:
	uv run main.py --config $(config)

refactor:
	uv run black src/
	uv run isort .

linters:
	uv run mypy .

tests:
	uv run pytest

setup:
	cp .env.local.example .env.local
	echo "Проверь локальные переменные в файле .env.local!"
	uv run pre-commit install
