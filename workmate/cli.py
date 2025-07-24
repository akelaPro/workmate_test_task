import argparse
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', nargs='+', required=True)
    parser.add_argument(
        '--report',
        choices=['average'],
        default='average',
        help='Report type (default: average)'
    )
    parser.add_argument(
        '--date',
        type=validate_date,
        help='Filter logs by date (YYYY-MM-DD)'
    )
    return parser.parse_args()


def validate_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        msg = f"Неправильный формат даты: {date_str}. Ожидается YYYY-MM-DD"
        raise argparse.ArgumentTypeError(msg)
