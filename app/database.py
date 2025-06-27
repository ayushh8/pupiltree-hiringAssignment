import json
from config import DATABASE_FILE

def get_bookings():
    """Retrieve all bookings from the database."""
    try:
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_booking(booking_details):
    """Save a new booking to the database."""
    bookings = get_bookings()
    bookings.append(booking_details)
    with open(DATABASE_FILE, "w") as f:
        json.dump(bookings, f, indent=4)

def update_booking(booking_id, updates):
    """Update an existing booking."""
    bookings = get_bookings()
    for booking in bookings:
        if booking.get("id") == booking_id:
            booking.update(updates)
            break
    with open(DATABASE_FILE, "w") as f:
        json.dump(bookings, f, indent=4) 