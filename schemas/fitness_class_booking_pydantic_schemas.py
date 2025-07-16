from pydantic import BaseModel, validator, Field
from datetime import datetime, timezone
import pytz

# time zone conf
ist_tz = pytz.timezone('Asia/Kolkata')

# Pydantic Models
class ClassBase(BaseModel):
    name: str
    instructor: str
    start_time: datetime
    end_time: datetime
    capacity: int

    @validator('start_time', 'end_time')
    def validate_datetime(cls, v):
        if v.tzinfo is None:

            v = ist_tz.localize(v)
        return v.astimezone(timezone.utc)


class ClassResponse(ClassBase):
    id: int
    available_slots: int

    class Config:
        from_attributes = True


class BookingRequest(BaseModel):
    class_id: int
    user_email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.[\w]+$')
    user_name: str = Field(..., min_length=1, max_length=100)


class BookingResponse(BaseModel):
    id: int
    class_id: int
    user_email: str
    user_name: str
    booking_time: datetime
    class_name: str
    class_start_time: datetime

    class Config:
        from_attributes = True

