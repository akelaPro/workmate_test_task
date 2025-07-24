import pytest
from unittest.mock import patch, MagicMock
from main import main

@patch('main.parse_args')
@patch('main.process_logs')
@patch('main.generate_report')
def test_main(mock_report, mock_process, mock_parse):
    args = MagicMock()
    args.file = ["file1.log"]
    args.report = "average"
    args.date = None
    mock_parse.return_value = args
    
    stats = {"test": {"count": 1, "total_time": 0.5}}
    mock_process.return_value = stats
    
    main()
    
    mock_parse.assert_called_once()
    mock_process.assert_called_once_with(["file1.log"], date_filter=None)
    mock_report.assert_called_once_with(stats, "average")