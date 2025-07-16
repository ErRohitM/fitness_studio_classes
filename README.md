# Fitness Studio Booking API

A comprehensive FastAPI-based booking system for fitness classes with timezone support and robust error handling.

## Features

- **Class Management**: View upcoming fitness classes
- **Booking System**: Book classes with validation and overbooking prevention
- **Timezone Support**: Automatic IST to any timezone conversion
- **Data Validation**: Pydantic models for request/response validation
- **Error Handling**: Comprehensive error responses with proper HTTP status codes
- **Logging**: Structured logging for debugging and monitoring
- **Database**: SQLite with proper datetime handling (UTC storage)

## Quick Start

### 1. Installation

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python seed_data.py
```

### 3. Run the Server

```bash
uvicorn main:app --reload
```

### 4. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### GET /classes
Get all fitness classes with timezone conversion.

**Query Parameters:**
- `timezone_param` (optional): Target timezone (default: Asia/Kolkata)
- `upcoming_only` (optional): Show only upcoming classes (default: true)

**Example:**
```bash
curl "http://localhost:8000/api/fitness_classes/classes?timezone_param=America/New_York"
```

### POST /book
Book a fitness class.

**Request Body:**
```json
{
  "class_id": 1,
  "user_email": "user@example.com",
  "user_name": "John Doe"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/fitness_classes/book" \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 1,
    "user_email": "john@example.com",
    "user_name": "John Doe"
  }'
```

### GET /bookings
Get user bookings by email.

**Query Parameters:**
- `email` (required): User email address
- `timezone_param` (optional): Target timezone (default: Asia/Kolkata)
- `include_cancelled` (optional): Include cancelled bookings (default: false)

**Example:**
```bash
curl "http://localhost:8000/api/fitness_classes/bookings?email=john@example.com"
```

## Architecture

### Database Design
- **UTC Storage**: All datetime values stored in UTC
- **Timezone Conversion**: Dynamic conversion to any timezone
- **Relationships**: Proper foreign key relationships between classes and bookings

## Testing

Run the test suite:
```bash
pytest test_api.py -v
```
