# CLI tool
import argparse # for parsing command-line arguments
from datetime import datetime
from src.parser import find_connected_hosts

def parse_args():
    parser = argparse.ArgumentParser(description="Find hosts connected to a target within a time window.")
    parser.add_argument("file", help="Path to the log file")
    parser.add_argument("host", help="Target host to search for")
    parser.add_argument("start", help="Start time (format: YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("end", help="End time (format: YYYY-MM-DD HH:MM:SS)")
    return parser.parse_args()

def main():
    args = parse_args()

    # Convert input time strings to datetime objects
    start_dt = datetime.strptime(args.start, "%Y-%m-%d %H:%M:%S")
    end_dt = datetime.strptime(args.end, "%Y-%m-%d %H:%M:%S")

    results = find_connected_hosts(args.file, args.host, start_dt, end_dt)

    if results:
        print(f"Hosts connected to '{args.host}' between {args.start} and {args.end}:")
        for r in results:
            print(f"- {r}")
    else:
        print(f"No connections found for '{args.host}' in the given time window.")

if __name__ == "__main__":
    main()
