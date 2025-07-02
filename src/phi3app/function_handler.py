"""
Function calling handler for the chatbot.
Contains logic for parsing function calls from model output and executing them.
"""

import re
from .agoda_functions import fetch_policy, fetch_booking_info, get_hotel_deals

# Function registry for dynamic calling
AVAILABLE_FUNCTIONS = {
    "fetch_policy": fetch_policy,
    "fetch_booking_info": fetch_booking_info,
    "get_hotel_deals": get_hotel_deals
}

def parse_function_call(text):
    """Parse function calls from model output"""
    # Look for pattern: CALL function_name("argument") or CALL function_name()
    pattern = r'CALL\s+(\w+)\s*\(\s*["\']?([^"\']*)["\']?\s*\)'
    matches = re.findall(pattern, text)
    
    function_calls = []
    for func_name, arg in matches:
        if func_name in AVAILABLE_FUNCTIONS:
            function_calls.append({
                'function': func_name,
                'argument': arg.strip() if arg else None
            })
    
    return function_calls

def execute_function_call(func_name, argument):
    """Execute a function call and return the result"""
    try:
        func = AVAILABLE_FUNCTIONS[func_name]
        if argument:
            return func(argument)
        else:
            return func()
    except Exception as e:
        return f"Error executing {func_name}: {str(e)}"

def get_system_context():
    """Get the system context with function calling instructions"""
    return """<|system|>
You are a helpful AI assistant for Agoda travel platform. You can call functions to get specific information.

Available functions:
- CALL fetch_policy("policy_type") - Get policy info (privacy, customer, cancellation, payment)
- CALL fetch_booking_info("booking_id") - Get booking details by ID (e.g., AG123456)
- CALL get_hotel_deals("destination") - Get current deals for a destination (optional)

When you need specific information, use the CALL format. Otherwise, provide helpful general responses.

Examples:
User: What's Agoda's privacy policy?
Assistant: Let me get that information for you.
CALL fetch_policy("privacy")

User: Check my booking AG123456
Assistant: I'll look up your booking details.
CALL fetch_booking_info("AG123456")<|end|>""" 