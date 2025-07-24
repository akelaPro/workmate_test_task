from workmate.reporter import generate_report, _prepare_average_report, _print_table
from collections import defaultdict
from io import StringIO
import sys

def test_prepare_average_report():
    stats = defaultdict(lambda: {'count': 0, 'total_time': 0.0})
    stats["/api"] = {"count": 10, "total_time": 5.0}
    stats["/home"] = {"count": 5, "total_time": 2.5}
    
    report_data = _prepare_average_report(stats)
    
    assert len(report_data) == 2
    assert report_data[0] == ["/api", 10, "0.500s"]
    assert report_data[1] == ["/home", 5, "0.500s"]
    assert report_data == sorted(report_data, key=lambda x: x[1], reverse=True)

def test_generate_report_average(capsys):
    stats = defaultdict(lambda: {'count': 0, 'total_time': 0.0})
    stats["/test"] = {"count": 2, "total_time": 1.0}
    
    generate_report(stats, "average")
    
    captured = capsys.readouterr()
    assert "/test" in captured.out
    assert "2" in captured.out
    assert "0.500s" in captured.out

def test_print_table(capsys):
    data = [["/test", 2, "0.500s"]]
    _print_table(data)
    
    captured = capsys.readouterr()
    assert "Endpoint" in captured.out
    assert "Requests" in captured.out
    assert "Avg Time" in captured.out
    assert "/test" in captured.out
    assert "2" in captured.out
    assert "0.500s" in captured.out