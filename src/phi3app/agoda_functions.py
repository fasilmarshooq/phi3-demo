"""
Agoda business logic functions for the chatbot.
Contains all the mock functions that simulate Agoda API calls.
"""

def fetch_policy(policy_type):
    """Fetch Agoda policy information"""
    policies = {
        "privacy": "Agoda's privacy policy: We protect your personal data and do not share it with third parties without your explicit consent. We use encryption and secure servers to safeguard your information.",
        "customer": "Agoda's customer policy: We strive for 100% customer satisfaction and offer 24/7 multilingual support. Our team assists with bookings, modifications, cancellations, and any issues during your stay.",
        "cancellation": "Agoda's cancellation policy: Cancellation terms vary by property. Many hotels offer free cancellation up to 24-48 hours before check-in. Non-refundable rates provide lower prices but no cancellation option.",
        "payment": "Agoda's payment policy: We accept major credit cards, PayPal, and local payment methods. Payment is processed securely with encryption. Some properties allow pay-at-hotel options."
    }
    return policies.get(policy_type.lower(), f"Policy type '{policy_type}' not found. Available policies: privacy, customer, cancellation, payment")

def fetch_booking_info(booking_id):
    """Fetch booking information by ID"""
    # Mock booking data
    bookings = {
        "AG123456": {"hotel": "Grand Palace Bangkok", "dates": "Dec 15-18, 2024", "status": "confirmed", "total": "$360"},
        "AG789012": {"hotel": "Marina Bay Sands", "dates": "Jan 5-8, 2025", "status": "pending", "total": "$1050"},
        "AG555999": {"hotel": "Park Hyatt Tokyo", "dates": "Feb 10-12, 2025", "status": "confirmed", "total": "$900"}
    }
    
    if booking_id in bookings:
        booking = bookings[booking_id]
        return f"Booking {booking_id}: {booking['hotel']} from {booking['dates']}, Status: {booking['status']}, Total: {booking['total']}"
    else:
        return f"Booking {booking_id} not found. Please check your booking ID."

def get_hotel_deals(destination=None):
    """Get current hotel deals"""
    deals = [
        {"destination": "Bangkok", "deal": "30% off luxury hotels", "code": "BANGKOK30", "valid_until": "Dec 31, 2024"},
        {"destination": "Singapore", "deal": "Free breakfast + 25% off", "code": "SINGAPORE25", "valid_until": "Jan 15, 2025"},
        {"destination": "Tokyo", "deal": "Book 3 nights, get 1 free", "code": "TOKYO3FOR2", "valid_until": "Mar 1, 2025"}
    ]
    
    if destination:
        matching_deals = [d for d in deals if destination.lower() in d['destination'].lower()]
        if matching_deals:
            deal = matching_deals[0]
            return f"{deal['destination']} deal: {deal['deal']} (Code: {deal['code']}, Valid until: {deal['valid_until']})"
        else:
            return f"No current deals found for {destination}. Check back later for new offers!"
    else:
        return "Current deals: " + " | ".join([f"{d['destination']}: {d['deal']} (Code: {d['code']})" for d in deals]) 