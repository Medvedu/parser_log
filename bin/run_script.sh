#!/bin/bash

if ! command -v uv &> /dev/null; then
  echo "Ошибка: команда 'uv' не найдена. Установите ее и повторите."
  exit 1
fi

if [[ ! -f main.py ]]; then
  echo "Ошибка: файл main.py не найден."
  exit 1
fi

# Можно через makefile запускать, однако утилита плохо поддерживает
# флаги, в частности, --config.
uv run main.py "$@"