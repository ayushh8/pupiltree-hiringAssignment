from langchain_core.tools import tool
from app.database import save_booking, update_booking, get_bookings
import datetime
import uuid

@tool
def get_hotel_info(query: str):
    """Provides information about the hotel, such as amenities, check-in/out times, and location."""
    # This is a mock tool. In a real application, you would fetch this from a database or API.
    if "amenities" in query.lower():
        return "We have a swimming pool, a gym, and a restaurant."
    if "check-in" in query.lower():
        return "Check-in is at 3 PM."
    if "check-out" in query.lower():
        return "Check-out is at 12 PM."
    if "location" in query.lower():
        return "We are located at 123 Main St."
    return "I'm sorry, I can't answer that question."

@tool
def book_hotel_room(check_in_date: str, check_out_date: str, room_type: str, num_guests: int):
    """Books a hotel room for the given dates, room type, and number of guests."""
    booking_id = str(uuid.uuid4())
    booking_details = {
        "id": booking_id,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "room_type": room_type,
        "num_guests": num_guests,
        "status": "confirmed",
    }
    save_booking(booking_details)
    return f"Booking confirmed! Your booking ID is {booking_id}."

@tool
def reschedule_booking(booking_id: str, new_check_in_date: str, new_check_out_date: str):
    """Reschedules an existing booking to new dates."""
    updates = {
        "check_in_date": new_check_in_date,
        "check_out_date": new_check_out_date,
    }
    update_booking(booking_id, updates)
    return f"Booking {booking_id} has been successfully rescheduled." 