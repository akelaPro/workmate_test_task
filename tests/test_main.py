from unittest.mock import patch, MagicMock
from main import main


class TestMain:
    """Тесты для основной функции main."""
    @patch('main.parse_args')
    @patch('main.process_logs')
    @patch('main.generate_report')
    def test_main(self, mock_report, mock_process, mock_parse):
        """Тест основной функции без фильтрации по дате."""
        args = MagicMock()
        args.file = ["file1.log"]
        args.report = "average"
        args.date = None
        mock_parse.return_value = args

        stats = {
            'aggregated': {"test": {"count": 1, "total_time": 0.5}},
            'raw_logs': []
        }
        mock_process.return_value = stats

        main()

        mock_parse.assert_called_once()
        mock_process.assert_called_once_with(["file1.log"], date_filter=None)
        mock_report.assert_called_once_with(stats, "average")

    @patch('main.parse_args')
    def test_main_with_date(self, mock_parse):
        """Тест основной функции с фильтрацией по дате."""
        args = MagicMock()
        args.file = ["file1.log"]
        args.report = "average"
        args.date = "2023-01-01"
        mock_parse.return_value = args
        with patch('main.process_logs') as mock_process, \
             patch('main.generate_report') as mock_report:
            main()
            mock_process.assert_called_once_with(["file1.log"], date_filter=args.date)