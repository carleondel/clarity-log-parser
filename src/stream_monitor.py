
from collections import deque, defaultdict
from datetime import datetime, timedelta, timezone
from src.utils import unix_to_datetime
from src.utils import datetime_to_unix

class StreamMonitor:
    def __init__(self, log_file, incoming_host, outgoing_host, frequency_seconds=3600):
        self.log_file = log_file
        self.incoming_host = incoming_host
        self.outgoing_host = outgoing_host
        self.frequency = frequency_seconds

        # Store log entries from the last hour (or N seconds)
        self.recent_logs = deque()  # stores tuples: (timestamp, src, dst)

        # Count total connections per host (bidirectional)
        self.total_connections = defaultdict(int)

        # Track incoming/outgoing separately
        self.incoming_connections = set()
        self.outgoing_connections = set()

    def add_line(self, line):
        parsed = self.parse_log_line(line)
        if not parsed:
            return

        timestamp, src, dst = parsed
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(seconds=self.frequency)

        if timestamp < window_start:
            return  # Skip old lines

        self.recent_logs.append((timestamp, src, dst))
        self.total_connections[src] += 1
        self.total_connections[dst] += 1

        if dst == self.incoming_host:
            self.incoming_connections.add(src)
        if src == self.outgoing_host:
            self.outgoing_connections.add(dst)

    def parse_log_line(self, line):
        try:
            parts = line.strip().split()
            timestamp = unix_to_datetime(int(parts[0]))
            src = parts[1]
            dst = parts[2]
            return timestamp, src, dst
        except Exception:
            return None

    def report(self):
        print(f"\n📊 Report at {datetime.now(timezone.utc).isoformat()}:")

        print(f"\n🔻 Hosts connected TO '{self.incoming_host}' (last hour):")
        for h in sorted(self.incoming_connections):
            print(f"- {h}")

        print(f"\n🔺 Hosts '{self.outgoing_host}' connected TO (last hour):")
        for h in sorted(self.outgoing_connections):
            print(f"- {h}")

        if self.total_connections:
            top_host = max(self.total_connections.items(), key=lambda x: x[1])
            print(f"\n🏆 Host with most connections: {top_host[0]} ({top_host[1]} connections)")
        else:
            print("\n🏆 No connections found yet.")

    def clear_old_entries(self):
        """Remove entries older than the current time window."""
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(seconds=self.frequency)

        while self.recent_logs and self.recent_logs[0][0] < cutoff:
            old_entry = self.recent_logs.popleft()
            _, src, dst = old_entry
            self.total_connections[src] -= 1
            self.total_connections[dst] -= 1

            if dst == self.incoming_host:
                self.incoming_connections.discard(src)
            if src == self.outgoing_host:
                self.outgoing_connections.discard(dst)

    def run_batch(self):
        """Read the whole log file once, simulating batch mode."""
        with open(self.log_file, "r") as f:
            for line in f:
                self.add_line(line)

        self.report()
