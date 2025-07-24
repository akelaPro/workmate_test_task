from tabulate import tabulate
from .base import Report

class AverageReport(Report):
    def generate(self, stats):
        data = sorted(
            [
                [url, data['count'], f"{data['total_time']/data['count']:.3f}s"]
                for url, data in stats.items()
            ],
            key=lambda x: x[1],
            reverse=True
        )
        headers = ["Endpoint", "Requests", "Avg Time"]
        print(tabulate(data, headers=headers, tablefmt="grid"))