from datetime import datetime, timedelta, timezone
import random


def generate_verification_code() -> int:
    return random.randint(100000, 999999)


def get_current_time() -> datetime:
    return datetime.now(tz=timezone.utc)
