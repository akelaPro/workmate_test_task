Workmate Log Analyzer
Анализирует лог-файлы и генерирует отчеты о времени ответа эндпоинтов.

Зависимости
Python 3.12

Poetry (для управления зависимостями)


Установка: make install

Запуск: poetry run python main.py --file path/to/logfile.log [--date YYYY-MM-DD]

Пример: poetry run python main.py --file file1.log file2.log --report average --date 2025-06-22clear


Тестирование
make test:  Запуск тестов
make lint: Проверка стиля кода (flake8)
make check-coverage: Проверка покрытия тестами


Пример работы

<a href="https://asciinema.org/a/Roz1cOiukx6kuvjSIoGvVrO8p" target="_blank"><img src="https://asciinema.org/a/Roz1cOiukx6kuvjSIoGvVrO8p.svg" /></a>