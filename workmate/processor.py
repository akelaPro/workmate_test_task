import json
import os
from collections import defaultdict
from datetime import datetime, date


def process_logs(files, date_filter=None):
    """Обрабатывает лог-файлы и возвращает статистику."""
    if not files:
        raise ValueError("Не указаны файлы для обработки")

    stats = {
        'aggregated': defaultdict(lambda: {'count': 0, 'total_time': 0.0}),
        'raw_logs': []
    }

    filter_date = date_filter
    if date_filter and not isinstance(date_filter, date):
        raise TypeError("date_filter должен быть объектом datetime.date")

    for file_path in files:
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Файл не найден: {file_path}"
            )

        if not os.path.isfile(file_path):
            raise ValueError(
                f"Указанный путь не является файлом: {file_path}"
            )

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        log = json.loads(line)

                        if 'url' not in log or 'response_time' not in log:
                            continue

                        if filter_date:
                            log_timestamp = log.get('@timestamp')
                            if not log_timestamp:
                                continue
                            try:
                                log_date = datetime.fromisoformat(
                                    log_timestamp
                                ).date()
                                if log_date != filter_date:
                                    continue
                            except (ValueError, TypeError):
                                continue

                        _update_stats(stats, log)

                    except json.JSONDecodeError as e:
                        msg = (
                            f"Ошибка в файле {file_path}, "
                            f"строка {line_num}: некорректный JSON - {e}"
                        )
                        print(msg)
                        continue

        except IOError as e:
            print(f"Ошибка чтения файла {file_path}: {e}")
            continue

    return stats


def _update_stats(stats, log):
    try:
        if 'url' not in log or 'response_time' not in log:
            return

        url = log['url']
        response_time = float(log['response_time'])
        stats['aggregated'][url]['count'] += 1
        stats['aggregated'][url]['total_time'] += response_time
        stats['raw_logs'].append(log)
    except (KeyError, ValueError):
        print(f"Ошибка обработки записи лога: {log.get('url', 'unknown')}")
