from datetime import datetime, timezone

def unix_to_datetime(ts: int) -> datetime:
    """Convert a UNIX timestamp (in seconds) to UTC datetime."""
    return datetime.fromtimestamp(ts, tz=timezone.utc)

def datetime_to_unix(dt: datetime) -> int:
    """Convert datetime to UNIX timestamp (seconds since JAN 01 1970 (UTC))."""
    return int(dt.replace(tzinfo=timezone.utc).timestamp())
