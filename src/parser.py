
from typing import List
from datetime import datetime


def find_connected_hosts(
    file_path: str,
    target_host: str,
    start_time: datetime,
    end_time: datetime
) -> List[str]:
    """
    Parse a log file and return a list of hostnames that connected
    to or from the target_host within a given time window.

    Args:
        file_path (str): Path to the log file
        target_host (str): The hostname to filter connections for
        start_time (datetime): Start of time window
        end_time (datetime): End of time window

    Returns:
        List[str]: Unique hostnames connected to the target host
    """
    connections = set() # to avoid duplicates in the hostnames
    ts_start = int(start_time.timestamp()) #converts datetimes to UNIX timestamps
    ts_end = int(end_time.timestamp())

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 3:
                continue  # skip malformed lines
            timestamp_str, src, dst = parts # <timestamp> <hostA> <hostB>
            try:
                timestamp = int(timestamp_str)
            except ValueError:
                continue

            if ts_start <= timestamp <= ts_end:
                if src == target_host:  # check if the host is involved in the connection (either as source or destination)
                    connections.add(dst) # we are assuming that the logs aren't directed, so if hostA connects to hostB, we consider both hosts connected to each other
                elif dst == target_host:
                    connections.add(src)

    return sorted(connections) # sort alphabetically
