
from datetime import datetime
from src.parser import find_connected_hosts

log_file = "data/Optional-connections.log"
hostname = "host80"
start_time = datetime.fromisoformat("2024-01-01T00:00:00")
end_time = datetime.fromisoformat("2024-12-31T23:59:59")

result = find_connected_hosts(log_file, hostname, start_time, end_time)

print(f"Connected hosts to {hostname} between {start_time} and {end_time}:")
print(result)
