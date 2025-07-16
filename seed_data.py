from datetime import datetime, timezone, timedelta
import pytz

from db_conn.db import SessionLocal
from models.fitness_class_booking_models import FitnessClass
from schemas.fitness_class_booking_pydantic_schemas import ist_tz


def seed_database():
    """Seed the database with sample fitness classes"""
    db = SessionLocal()

    # Clear existing data
    db.query(FitnessClass).delete()
    db.commit()

    # Sample classes
    classes = [
        {
            "name": "Morning Yoga",
            "instructor": "Sarah Johnson",
            "start_time": ist_tz.localize(datetime(2025, 7, 16, 7, 0)),
            "end_time": ist_tz.localize(datetime(2025, 7, 16, 8, 0)),
            "capacity": 20
        },
        {
            "name": "HIIT Training",
            "instructor": "Mike Chen",
            "start_time": ist_tz.localize(datetime(2025, 7, 16, 18, 0)),
            "end_time": ist_tz.localize(datetime(2025, 7, 16, 19, 0)),
            "capacity": 30
        },
        {
            "name": "Pilates",
            "instructor": "Emma Wilson",
            "start_time": ist_tz.localize(datetime(2025, 7, 17, 10, 0)),
            "end_time": ist_tz.localize(datetime(2025, 7, 17, 11, 0)),
            "capacity": 3
        },
        {
            "name": "Strength Training",
            "instructor": "David Kumar",
            "start_time": ist_tz.localize(datetime(2025, 7, 17, 16, 0)),
            "end_time": ist_tz.localize(datetime(2025, 7, 17, 17, 30)),
            "capacity": 10
        },
        {
            "name": "Zumba Dance",
            "instructor": "Maria Rodriguez",
            "start_time": ist_tz.localize(datetime(2025, 7, 18, 19, 0)),
            "end_time": ist_tz.localize(datetime(2025, 7, 18, 20, 0)),
            "capacity": 25
        }
    ]

    for class_data in classes:
        # Convert to UTC for storage
        start_utc = class_data["start_time"].astimezone(pytz.utc)
        end_utc = class_data["end_time"].astimezone(pytz.utc)

        db_class = FitnessClass(
            name=class_data["name"],
            instructor=class_data["instructor"],
            start_time=start_utc,
            end_time=end_utc,
            capacity=class_data["capacity"]
        )
        db.add(db_class)

    db.commit()
    db.close()
    print("Database seeded successfully!")


if __name__ == "__main__":
    seed_database()