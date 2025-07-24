from workmate.cli import parse_args
from workmate.processor import process_logs
from workmate.reporter import generate_report



def main():
    args = parse_args()
    stats = process_logs(args.file, date_filter=args.date)
    generate_report(stats, args.report)

if __name__ == "__main__":
    main()
    