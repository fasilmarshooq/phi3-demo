"""
Phi-3 chatbot with Agoda function calling capabilities.
"""

from .chat import chat
from .agoda_functions import fetch_policy, fetch_booking_info, get_hotel_deals
from .function_handler import parse_function_call, execute_function_call

__version__ = "0.1.0"
__all__ = ["chat", "fetch_policy", "fetch_booking_info", "get_hotel_deals", "parse_function_call", "execute_function_call"]
