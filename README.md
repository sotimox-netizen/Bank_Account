# Bank.ProjectZ 

> Лабораторная работа 

## О проекте

Учебный проект, демонстрирующий правильную структуру Python-пакета с инкапсуляцией, кастомными исключениями, логированием.

## Структура проекта

```
Bank.ProjectZ/
├── src/
│   ├── bank_account/
│   │   ├── account.py       # Класс BankAccount
│   │   └── exceptions.py    # Кастомные исключения
│   └── core/
│       └── config.py        # Конфигурация (заглушка)
├── tests/
│   └── bank_account/
│       └── test_account.py  # 22 теста, покрытие 100%
├── scripts/
│   ├── seed_account.py      # Генерация тестовых счетов
│   └── demo.py              # Интерактивное демо
├── logs/                    # Директория для логов
├── pyproject.toml           # Конфигурация проекта и инструментов
└── .gitignore
```

## Установка

```bash
# Клонировать репозиторий
git clone https://github.com/sotimox-netizen/Bank.ProjectZ.git
cd Bank.ProjectZ

# Установить пакет в режиме разработки
pip install -e ".[dev]"
```

## Запуск

```bash
# Демо с тестовыми счетами
python3 scripts/seed_account.py

# Интерактивный режим
python3 scripts/demo.py
```

## Тесты

```bash
pytest
```
## Технологии

- Python 3.9+
- `pytest` + `pytest-cov` — тестирование
- `black` — форматирование кода
- `isort` — сортировка импортов
- `mypy` — статическая типизация
