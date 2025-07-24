# tests/test_processor.py
import pytest
from workmate.processor import process_logs, _update_stats
from datetime import date
from collections import defaultdict

class TestProcessLogs:
    @pytest.fixture
    def sample_logs(self, tmp_path):
        file1 = tmp_path / "file1.log"
        file1.write_text(
            '{"url": "/api", "response_time": 0.1, "@timestamp": "2023-01-01T00:00:00"}\n'
            '{"url": "/api", "response_time": 0.2, "@timestamp": "2023-01-02T00:00:00"}\n'
            '{"url": "/home", "response_time": 0.05, "@timestamp": "2023-01-02T00:00:00"}\n'
        )
        file2 = tmp_path / "file2.log"
        file2.write_text(
            '{"url": "/api", "response_time": 0.15, "@timestamp": "2023-01-03T00:00:00"}\n'
            '{"url": "/about", "response_time": 0.3, "@timestamp": "2023-01-03T00:00:00"}\n'
        )
        return [str(file1), str(file2)]

    def test_process_logs(self, sample_logs):
        stats = process_logs(sample_logs)
        aggregated = stats['aggregated']
        
        assert set(aggregated.keys()) == {"/api", "/home", "/about"}
        assert aggregated["/api"]["count"] == 3
        assert aggregated["/api"]["total_time"] == pytest.approx(0.45)
        assert len(stats['raw_logs']) == 5

    def test_date_filter(self, sample_logs):
        stats = process_logs(sample_logs, date_filter=date(2023, 1, 1))
        assert stats['aggregated']["/api"]["count"] == 1
        assert len(stats['raw_logs']) == 1

    def test_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            process_logs(["nonexistent.log"])

    def test_invalid_file(self, tmp_path):
        invalid_file = tmp_path / "invalid.log"
        invalid_file.write_text("invalid json\n")
        
        stats = process_logs([str(invalid_file)])
        assert len(stats['aggregated']) == 0


    def test_update_stats(self):
        stats = {
            'aggregated': defaultdict(lambda: {'count': 0, 'total_time': 0.0}),
            'raw_logs': []
        }
        _update_stats(stats, {"url": "/test", "response_time": 0.5})
        assert stats['aggregated']["/test"]["count"] == 1

    def test_incomplete_log(self):
        stats = defaultdict(lambda: {'count': 0, 'total_time': 0.0})
        _update_stats(stats, {"url": "/test"})
        assert stats["/test"]["count"] == 0