from datetime import datetime, timezone
import logging
import pytz

from db_conn.db import SessionLocal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def convert_to_timezone(dt: datetime, target_tz: str, as_string: bool = False) -> datetime | str:
    """
    Converts a datetime from UTC to the target timezone.

    Args:
        dt (datetime): The input datetime (naive or UTC-aware).
        target_tz (str): The IANA timezone string (e.g., "Asia/Kolkata").
        as_string (bool): If True, returns ISO 8601 string with offset.

    Returns:
        datetime or str: Timezone-aware datetime or formatted string.
    """
    try:
        # Ensures datetime is timezone-aware in UTC
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        else:
            dt = dt.astimezone(pytz.utc)

        # Validates and apply target timezone
        if target_tz not in pytz.all_timezones:
            raise ValueError(f"Invalid timezone: {target_tz}")

        target_timezone = pytz.timezone(target_tz)
        converted = dt.astimezone(target_timezone)

        return converted.isoformat() if as_string else converted

    except Exception as e:
        logger.error(f"Timezone conversion failed: {e}")
        return dt  # Fallback to original