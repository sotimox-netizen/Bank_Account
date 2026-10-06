"""organizer.py — скрипт для наведения порядка в директории.

Принимает путь к директории (по умолчанию — текущая рабочая директория),
раскладывает файлы по подкаталогам-категориям (Documents, Images, Audio,
Video, Archives, Other) в зависимости от расширения и печатает отчёт.

Используются только стандартные модули os и sys (без shutil).
"""

import os
import sys

# Категории файлов: имя категории -> множество расширений (в нижнем регистре, с точкой)
CATEGORIES = {
    "Documents": {".txt", ".pdf", ".docx", ".md"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp"},
    "Audio": {".mp3", ".wav", ".flac", ".aac"},
    "Video": {".mp4", ".avi", ".mkv", ".mov"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
}

OTHER_CATEGORY = "Other"


def get_target_directory(argv):
    """Разбирает аргументы командной строки и возвращает путь к директории.

    Если аргумент не передан, используется текущая рабочая директория.
    Проверяет, что путь существует и является директорией; иначе —
    понятное сообщение об ошибке и завершение с ненулевым кодом возврата.
    """
    if len(argv) > 1:
        path = argv[1]
    else:
        path = os.getcwd()

    if not os.path.exists(path):
        print(f"Ошибка: путь не существует: {path}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(path):
        print(f"Ошибка: путь не является директорией: {path}", file=sys.stderr)
        sys.exit(1)

    return path


def get_category(filename):
    """Возвращает имя категории для файла по его расширению (регистр не важен)."""
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return OTHER_CATEGORY


def safe_move(src, dst_dir):
    """Безопасно перемещает файл src в директорию dst_dir через os.rename.

    При конфликте имён добавляет суффикс _1, _2, ... до расширения,
    чтобы не перезаписать существующий файл.

    Возвращает итоговое полное имя целевого файла либо None, если
    перемещение не удалось (исключение при os.rename).
    """
    base_name = os.path.basename(src)
    name, ext = os.path.splitext(base_name)

    counter = 0
    while True:
        if counter == 0:
            candidate = os.path.join(dst_dir, base_name)
        else:
            candidate = os.path.join(dst_dir, f"{name}_{counter}{ext}")

        if not os.path.exists(candidate):
            try:
                os.rename(src, candidate)
                return candidate
            except OSError:
                return None

        counter += 1


def categorize_files(directory):
    """Анализирует содержимое директории (только файлы верхнего уровня).

    Распределяет файлы по категориям и перемещает их в соответствующие
    подкаталоги. Подкаталоги создаются только при наличии файлов для
    перемещения. Скрипт organizer.py игнорируется.

    Возвращает словарь статистики:
        {"moved": {категория: количество}, "skipped": количество,
         "total": общее число обработанных файлов}
    """
    stats = {"moved": {}, "skipped": 0, "total": 0}

    script_name = os.path.basename(__file__)

    entries = sorted(os.listdir(directory))
    files = [
        e for e in entries
        if os.path.isfile(os.path.join(directory, e)) and e != script_name
    ]

    if not files:
        print(f"Директория '{directory}' пуста (нет файлов для обработки).")
        return stats

    for filename in files:
        stats["total"] += 1
        category = get_category(filename)
        dst_dir = os.path.join(directory, category)

        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)

        src = os.path.join(directory, filename)
        result = safe_move(src, dst_dir)

        if result is not None:
            stats["moved"][category] = stats["moved"].get(category, 0) + 1
        else:
            stats["skipped"] += 1

    return stats


def print_report(directory, stats):
    """Выводит итоговый отчёт в консоль."""
    print("=" * 50)
    print("Отчёт об организации файлов")
    print("=" * 50)
    print(f"Обработанная директория: {os.path.abspath(directory)}")
    print("-" * 50)

    total_moved = 0
    all_categories = list(CATEGORIES.keys()) + [OTHER_CATEGORY]
    for category in all_categories:
        count = stats["moved"].get(category, 0)
        total_moved += count
        print(f"{category:<12}: перемещено файлов - {count}")

    print("-" * 50)
    print(f"Всего перемещено: {total_moved}")
    print(f"Всего обработано файлов: {stats['total']}")
    print(f"Пропущено файлов (конфликты/ошибки): {stats['skipped']}")
    print("=" * 50)


def main():
    directory = get_target_directory(sys.argv)

    # Проверка на пустую директорию до создания подкаталогов
    has_files = any(
        os.path.isfile(os.path.join(directory, e))
        and e != os.path.basename(__file__)
        for e in os.listdir(directory)
    )
    if not has_files:
        print(f"Директория '{os.path.abspath(directory)}' пуста — ничего обрабатывать не нужно.")
        sys.exit(0)

    stats = categorize_files(directory)
    print_report(directory, stats)


if __name__ == "__main__":
    main()
