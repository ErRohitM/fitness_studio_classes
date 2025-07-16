from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from db_conn.db import Base, engine


class FitnessClass(Base):
    __tablename__ = "fitness_classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    instructor = Column(String)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    capacity = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    bookings = relationship("Booking", back_populates="fitness_class")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("fitness_classes.id"))
    user_email = Column(String, index=True)
    user_name = Column(String)
    booking_time = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    is_cancelled = Column(Boolean, default=False)

    fitness_class = relationship("FitnessClass", back_populates="bookings")


# Create tables
Base.metadata.create_all(bind=engine)
