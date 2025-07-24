import pytest
from collections import defaultdict
from workmate.processor import process_logs, _update_stats
from datetime import datetime, date

@pytest.fixture
def sample_logs(tmp_path):
    file1 = tmp_path / "file1.log"
    file1.write_text(
        '{"url": "/api", "response_time": 0.1, "@timestamp": "2023-01-01T00:00:00+00:00"}\n'
        '{"url": "/api", "response_time": 0.2, "@timestamp": "2023-01-02T00:00:00+00:00"}\n'
        '{"url": "/home", "response_time": 0.05, "@timestamp": "2023-01-02T00:00:00+00:00"}\n'
    )
    file2 = tmp_path / "file2.log"
    file2.write_text(
        '{"url": "/api", "response_time": 0.15, "@timestamp": "2023-01-03T00:00:00+00:00"}\n'
        '{"url": "/about", "response_time": 0.3, "@timestamp": "2023-01-03T00:00:00+00:00"}\n'
    )
    return [str(file1), str(file2)]

def test_process_logs(sample_logs):
    stats = process_logs(sample_logs)
    
    assert set(stats.keys()) == {"/api", "/home", "/about"}
    assert stats["/api"]["count"] == 3
    assert stats["/api"]["total_time"] == pytest.approx(0.45)
    assert stats["/home"]["count"] == 1
    assert stats["/about"]["count"] == 1

def test_process_logs_with_date_filter(sample_logs):
    date_filter = date(2023, 1, 1)
    stats = process_logs(sample_logs, date_filter=date_filter)
    assert set(stats.keys()) == {"/api"}
    assert stats["/api"]["count"] == 1
    assert stats["/api"]["total_time"] == pytest.approx(0.1)


def test_update_stats():
    stats = defaultdict(lambda: {'count': 0, 'total_time': 0.0})
    log1 = {"url": "/test", "response_time": 0.5}
    _update_stats(stats, log1)
    
    assert stats["/test"]["count"] == 1
    assert stats["/test"]["total_time"] == 0.5
    
    log2 = {"url": "/test", "response_time": 0.3}
    _update_stats(stats, log2)
    
    assert stats["/test"]["count"] == 2
    assert stats["/test"]["total_time"] == 0.8

def test_update_stats_incomplete_log():
    stats = defaultdict(lambda: {'count': 0, 'total_time': 0.0})
    log = {"url": "/test"}
    _update_stats(stats, log)
    
    assert stats["/test"]["count"] == 0
    assert stats["/test"]["total_time"] == 0.0