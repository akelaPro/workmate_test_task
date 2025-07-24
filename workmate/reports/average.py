from tabulate import tabulate
from .base import BaseReport


class AverageReport(BaseReport):
    """Отчёт со средней скоростью ответа по endpoint"""

    def generate(self, stats):
        aggregated_stats = stats.get('aggregated', {})
        data = self._prepare_data(aggregated_stats)
        self._print_table(data)

    def _prepare_data(self, stats):
        return sorted(
            [
                [url, data['count'],
                    f"{data['total_time']/data['count']:.3f}s"]
                for url, data in stats.items()
                if data['count'] > 0
            ],
            key=lambda x: x[1],
            reverse=True
        )

    def _print_table(self, data):
        headers = ["Endpoint", "Requests", "Avg Time"]
        print(tabulate(data, headers=headers, tablefmt="grid"))
