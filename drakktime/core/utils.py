from datetime import datetime


def parse_time(value: str) -> datetime:
    return datetime.strptime(value, "%H:%M")


def minutes_between(start: datetime, end: datetime) -> int:
    return int((end - start).total_seconds() // 60)


def format_minutes(total_minutes: int) -> str:
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours:02d}:{minutes:02d}"
