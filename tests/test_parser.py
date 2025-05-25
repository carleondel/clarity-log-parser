
from src.parser import find_connected_hosts
from datetime import datetime
import os


def test_find_connected_hosts():
    test_file = "tests/test_log.log"

    # Create a temporary test log file
    with open(test_file, "w") as f:
        f.write(
            "1704068314 host22 host29\n"
            "1704072476 host29 host35\n"
            "1704073616 host35 host22\n"
        )

    start = datetime.fromtimestamp(1704068000)
    end = datetime.fromtimestamp(1704075000)

    result = find_connected_hosts(test_file, "host22", start, end)
    assert set(result) == {"host29", "host35"}

    os.remove(test_file)
