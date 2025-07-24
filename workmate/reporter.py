from tabulate import tabulate

def generate_report(stats, report_type):
    if report_type == 'average':
        data = _prepare_average_report(stats)
        _print_table(data)

def _prepare_average_report(stats):
    return sorted(
        [
            [url, data['count'], f"{data['total_time']/data['count']:.3f}s"]
            for url, data in stats.items()
        ],
        key=lambda x: x[1],
        reverse=True
    )

def _print_table(data):
    headers = ["Endpoint", "Requests", "Avg Time"]
    print(tabulate(data, headers=headers, tablefmt="grid"))