# tests/test_reporter.py
import pytest
from workmate.reporter import generate_report
from workmate.reports.average import AverageReport
from collections import defaultdict

class TestAverageReport:
    @pytest.fixture
    def sample_stats(self):
        return {
            'aggregated': {
                "/api": {"count": 10, "total_time": 5.0},
                "/home": {"count": 5, "total_time": 2.5}
            },
            'raw_logs': []
        }

    def test_prepare_data(self, sample_stats):
        report = AverageReport()
        data = report._prepare_data(sample_stats['aggregated'])
        
        assert len(data) == 2
        assert data[0] == ["/api", 10, "0.500s"]
        assert data[1] == ["/home", 5, "0.500s"]
        assert data == sorted(data, key=lambda x: x[1], reverse=True)

    def test_generate_report(self, sample_stats, capsys):
        report = AverageReport()
        report.generate(sample_stats)
        
        captured = capsys.readouterr()
        assert "Endpoint" in captured.out
        assert "Requests" in captured.out
        assert "Avg Time" in captured.out
        assert "/api" in captured.out
        assert "/home" in captured.out

    def test_empty_stats(self):
        stats = {
            'aggregated': defaultdict(lambda: {'count': 0, 'total_time': 0.0}),
            'raw_logs': []
        }
        
        report = AverageReport()
        data = report._prepare_data(stats['aggregated'])
        assert len(data) == 0

    def test_zero_requests(self):
        stats = {
            'aggregated': {"/test": {"count": 0, "total_time": 0.0}},
            'raw_logs': []
        }
        
        report = AverageReport()
        data = report._prepare_data(stats['aggregated'])
        assert len(data) == 0


class TestReportFactory:
    def test_generate_average_report(self, capsys):
        stats = {
            'aggregated': {"/test": {"count": 2, "total_time": 1.0}},
            'raw_logs': []
        }
        
        generate_report(stats, "average")
        captured = capsys.readouterr()
        assert "/test" in captured.out
        assert "0.500s" in captured.out

    def test_unknown_report_type(self):
        with pytest.raises(ValueError, match="Unknown report type"):
            generate_report({}, "unknown_type")