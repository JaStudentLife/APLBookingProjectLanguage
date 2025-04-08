#Danielle Johns  - 2101310
#Deandre Powell - 2000819
#Carl Bruce - 2102246
#Shavar Morgan - 2100962

import ply.yacc as yacc
from lexer import tokens
from llm import fetch_events_from_gemini
from llm import fetch_from_gemini
reservations = {}


def p_command_book(p):
    'command : BOOK NUMBER TICKETS TO NAME ON DATE'
    tickets = p[2]
    event = p[5]
    date = p[7]

    print(f"Checking availability and info for {event} on {date}...")
    response = fetch_from_gemini(
        f"A user is booking {tickets} ticket(s) to {event} on {date} in Jamaica. "
        f"Please confirm if this event is likely to exist on that date, "
        f"and provide seat availability, location, or pricing if possible. If there is no available information,"
        f" make something up and let the user know. Makke sure to write it in a user friedly way"
    )
    print(response)
    reservations[event] = {'tickets': tickets, 'date': date, 'status': 'reserved'}
    print(f"Reserved {tickets} ticket(s) to {event} on {date}.")


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

def p_command_help(p):
    'command : HELP'
    print("""
Available commands:
BOOK [number] TICKETS TO [event] ON [date]
CONFIRM [event] FOR [name]
PAY [event] FOR [name]
CANCEL [event] FOR [name]
LIST [service] SCHEDULE
LIST [service] ROUTE FROM [origin] TO [destination]

Examples:
BOOK 2 TICKETS TO "Reggae Concert" ON "2025-05-15"
LIST Knutsford Express SCHEDULE
LIST Knutsford Express ROUTE FROM Kingston TO Montego Bay""")


def p_error(p):
    print("Syntax error!")

parser = yacc.yacc()
