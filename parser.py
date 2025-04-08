import ply.yacc as yacc
from lexer import tokens
from llm import fetch_events_from_gemini, fetch_from_gemini, provide_syntax_correction

reservations = {}

def p_command_book(p):
    'command : BOOK NUMBER TICKETS TO NAME ON DATE AT TIME FOR NAME'
    tickets = p[2]
    event = p[5]
    date = p[7]
    time = p[9]
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

def p_command_route(p):
    'command : LIST NAME ROUTE FROM NAME TO NAME'
    resource = p[2]
    origin = p[4]
    destination = p[6]
    print(f"Fetching route for {resource} from {origin} to {destination}...")
    response = fetch_events_from_gemini(f"List route for {resource} from {origin} to {destination} in Jamaica.")
    print(response)

def p_command_list(p):
    'command : LIST NAME SCHEDULE'
    resource = p[2]
    print(f"Fetching schedule for {resource}...")
    response = fetch_events_from_gemini(f"List schedule for {resource} in Jamaica with time and date.")
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
Book Knutsford Express from Montego Bay to Kingston on February 17, 2025 at 8:30 AM for Joy
Reynolds.
Confirm reservation for Knutsford Express for Joy Reynolds.
Pay reservation for Knutsford Express for Joy Reynolds.
""")

def p_error(p):
    if p:
        user_input = p.value

        print("Syntax error detected!")
        print(f"Sending the command to Gemini for correction: {user_input}")

        corrected_command = provide_syntax_correction(user_input)

        print("Gemini suggests the following correction:")
        print(corrected_command)
    else:
        print("Unexpected error: No input received.")

parser = yacc.yacc()
