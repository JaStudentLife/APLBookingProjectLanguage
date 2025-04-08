import ply.yacc as yacc
from lexer import tokens
from llm import fetch_events_from_gemini, fetch_from_gemini

reservations = {}


def p_command_book(p):
    'command : BOOK NUMBER TICKETS TO EVENT ON DATE AT TIME AM_PM FOR NAME'
    tickets = p[2]
    event = p[5]
    date = p[7]
    time = f"{p[9]} {p[10]}"
    name = p[11]

    print(f"Checking availability and info for {event} on {date} at {time}...")
    response = fetch_from_gemini(
        f"A user is booking {tickets} ticket(s) to {event} on {date} at {time} in Jamaica. "
        f"Please confirm if this event is likely to exist on that date, "
        f"and provide seat availability, location, or pricing if possible. If there is no available information,"
        f" make something up and let the user know. Make sure to write it in a user-friendly way."
    )
    print(response)
    reservations[event] = {'tickets': tickets, 'date': date, 'time': time, 'status': 'reserved', 'name': name}
    print(f"Reserved {tickets} ticket(s) to {event} on {date} at {time} for {name}.")

def p_command_confirm(p):
    'command : CONFIRM NAME FOR NAME'
    event = p[2]
    name = p[4]
    if event in reservations:
        reservations[event]['status'] = 'confirmed'
        reservations[event]['name'] = name
        print(f"Confirmed {event} for {name}.")
    else:
        print(f"No reservation found for {event}.")

def p_command_pay(p):
    'command : PAY NAME FOR NAME'
    event = p[2]
    name = p[4]
    if event in reservations and reservations[event].get('name') == name:
        reservations[event]['status'] = 'paid'
        print(f"Payment processed for {event} reserved by {name}.")
    else:
        print(f"Cannot process payment for {event}.")

def p_command_cancel(p):
    'command : CANCEL NAME FOR NAME'
    event = p[2]
    name = p[4]

    if event in reservations and reservations[event].get('name') == name:
        print(f"Checking refund/cancellation policy for {event}...")
        response = fetch_from_gemini(
            prompt=f"A user named {name} wants to cancel their reservation for {event}. "
                   f"Please explain any cancellation policy or refund rule, as if this were a real ticket booking system.",
        )
        print("Gemini says:")
        print(response)

        reservations[event]['status'] = 'cancelled'
        print(f"Cancelled reservation for {event} by {name}.")
    else:
        print("No reservation found.")

def p_command_list(p):
    'command : LIST NAME SCHEDULE'
    resource = p[2]
    print(f"Fetching schedule for {resource}...")
    response = fetch_events_from_gemini(f"List schedule for {resource} in Jamaica with time and date.")
    print(response)

def p_command_route(p):
    'command : LIST NAME ROUTE FROM NAME TO NAME'
    resource = p[2]
    origin = p[4]
    destination = p[6]
    print(f"Fetching route for {resource} from {origin} to {destination}...")
    response = fetch_events_from_gemini(f"List route for {resource} from {origin} to {destination} in Jamaica.")
    print(response)


def p_command_help(p):
    'command : HELP'
    print("""
Available commands:
BOOK [number] TICKETS TO [event] ON [date] AT [time] FOR [name]
CONFIRM [event] FOR [name]
PAY [event] FOR [name]
CANCEL [event] FOR [name]
LIST [service] SCHEDULE
LIST [service] ROUTE FROM [origin] TO [destination]

Examples:
List Knutsford Express schedule.
Book 2 tickets to Reggae Sumfest on February 17, 2025 at 8:30 AM for Joy Reynolds.
Confirm reservation for Knutsford Express for Joy Reynolds.
Pay reservation for Knutsford Express for Joy Reynolds.
""")


import ply.yacc as yacc
from lexer import tokens
from llm import provide_syntax_correction  # Use the correct function to call Gemini

def p_error(p):
    if p:
        user_input = p.lexer.lexdata

        print(f"Syntax error in input: '{user_input}'")

        prompt = f"User input: '{user_input}' has a syntax error. Can you suggest a way to fix it and show the correct syntax?"
        corrected_command = provide_syntax_correction(user_input)

        print("Gemini suggests the following correction:")
        print(corrected_command)

        print("Type 'help' to see available commands and examples.")
    else:
        print("Unexpected error: No input received.")


parser = yacc.yacc()