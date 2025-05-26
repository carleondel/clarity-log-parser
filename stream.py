import argparse
from src.stream_monitor import StreamMonitor

def parse_arguments():
    parser = argparse.ArgumentParser(description="Stream Monitor CLI")
    parser.add_argument("--logfile", type=str, required=True, help="Path to the log file")
    parser.add_argument("--incoming", type=str, required=True, help="Target host to monitor incoming connections")
    parser.add_argument("--outgoing", type=str, required=True, help="Target host to monitor outgoing connections")
    parser.add_argument("--frequency", type=int, default=3600, help="Frequency window in seconds (default: 3600)")

    return parser.parse_args()

def main():
    args = parse_arguments()

    monitor = StreamMonitor(
        log_file=args.logfile,
        incoming_host=args.incoming,
        outgoing_host=args.outgoing,
        frequency_seconds=args.frequency,
    )
    monitor.run_batch()

if __name__ == "__main__":
    main()
