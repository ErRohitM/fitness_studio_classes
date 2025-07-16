from fastapi import Query, Depends, HTTPException, APIRouter

from utils.dependencies import get_db, convert_to_timezone, logger
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from typing import List

from models.fitness_class_booking_models import FitnessClass, Booking
from schemas.fitness_class_booking_pydantic_schemas import ClassResponse, BookingResponse, BookingRequest


router = APIRouter(prefix="/api/fitness_classes", tags=["utils"])

@router.get("/")
async def root():
    return {"message": "Fitness Studio Booking API", "version": "1.0.0"}


@router.get("/classes", response_model=List[ClassResponse])
async def get_classes(
        timezone_param: str = Query("Asia/Kolkata", description="Target timezone for datetime conversion"),
        upcoming_only: bool = Query(True, description="Show only upcoming classes"),
        db: Session = Depends(get_db)
):
    """
    Get all fitness classes with timezone conversion
    """
    try:
        query = db.query(FitnessClass)

        if upcoming_only:
            query = query.filter(FitnessClass.start_time > datetime.now(timezone.utc))

        classes = query.all()

        result = []
        for cls in classes:
            # Count available slots
            active_bookings = db.query(Booking).filter(
                Booking.class_id == cls.id,
                Booking.is_cancelled == False
            ).count()

            available_slots = cls.capacity - active_bookings

            result.append(ClassResponse(
                id=cls.id,
                name=cls.name,
                instructor=cls.instructor,
                start_time=convert_to_timezone(cls.start_time, timezone_param, as_string=True),
                end_time=convert_to_timezone(cls.end_time, timezone_param, as_string=True),
                capacity=cls.capacity,
                available_slots=available_slots
            ))

        logger.info(f"Retrieved {len(result)} classes")
        return result

    except Exception as e:
        logger.error(f"Error retrieving classes: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/book", response_model=BookingResponse)
async def book_class(
        booking: BookingRequest,
        db: Session = Depends(get_db)
):
    """
    Book a fitness class
    """
    try:
        # Check if class exists
        fitness_class = db.query(FitnessClass).filter(FitnessClass.id == booking.class_id).first()
        if not fitness_class:
            raise HTTPException(status_code=404, detail="Class not found")

        # Check if class is in the future
        timezone_param = Query("Asia/Kolkata", description="Target timezone for datetime conversion"),
        if convert_to_timezone(fitness_class.start_time , timezone_param, as_string=True) <= datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Cannot book past classes")

        # Check if user already booked this class
        existing_booking = db.query(Booking).filter(
            Booking.class_id == booking.class_id,
            Booking.user_email == booking.user_email,
            Booking.is_cancelled == False
        ).first()

        if existing_booking:
            raise HTTPException(status_code=400, detail="User already booked this class")

        # Check available slots
        active_bookings = db.query(Booking).filter(
            Booking.class_id == booking.class_id,
            Booking.is_cancelled == False
        ).count()

        if active_bookings >= fitness_class.capacity:
            raise HTTPException(status_code=400, detail="Class is fully booked")

        # Create booking
        db_booking = Booking(
            class_id=booking.class_id,
            user_email=booking.user_email,
            user_name=booking.user_name,
            booking_time=datetime.now(timezone.utc)
        )

        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)

        logger.info(f"Booking created: {db_booking.id} for user {booking.user_email}")

        return BookingResponse(
            id=db_booking.id,
            class_id=db_booking.class_id,
            user_email=db_booking.user_email,
            user_name=db_booking.user_name,
            booking_time=db_booking.booking_time,
            class_name=fitness_class.name,
            class_start_time=fitness_class.start_time
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating booking: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/bookings", response_model=List[BookingResponse])
async def get_bookings(
        email: str = Query(..., description="User email to filter bookings"),
        timezone_param: str = Query("Asia/Kolkata", description="Target timezone for datetime conversion"),
        include_cancelled: bool = Query(False, description="Include cancelled bookings"),
        db: Session = Depends(get_db)
):
    """
    Get bookings by user email
    """
    try:
        query = db.query(Booking).join(FitnessClass).filter(Booking.user_email == email)

        if not include_cancelled:
            query = query.filter(Booking.is_cancelled == False)

        bookings = query.all()

        result = []
        for booking in bookings:


            result.append(BookingResponse(
                id=booking.id,
                class_id=booking.class_id,
                user_email=booking.user_email,
                user_name=booking.user_name,
                booking_time=convert_to_timezone(booking.booking_time, timezone_param, as_string=True),
                class_name=booking.fitness_class.name,
                class_start_time=convert_to_timezone(booking.fitness_class.start_time, timezone_param, as_string=True)
            ))

        logger.info(f"Retrieved {len(result)} bookings for {email}")
        return result

    except Exception as e:
        logger.error(f"Error retrieving bookings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

