from workmate.reports.average import AverageReport

def generate_report(stats, report_type='average'):
    """Фабрика отчётов"""
    report_classes = {
        'average': AverageReport,
    }
    
    if report_type not in report_classes:
        raise ValueError(f"Unknown report type: {report_type}")
    
    report = report_classes[report_type]()
    report.generate(stats)  # Передаём весь stats