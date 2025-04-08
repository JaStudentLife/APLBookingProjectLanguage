import ply.lex as lex

tokens = (
    'BOOK', 'CONFIRM', 'PAY', 'CANCEL', 'LIST',
    'NUMBER', 'TICKETS', 'TO', 'ON', 'EVENT',
    'FOR', 'NAME', 'SCHEDULE', 'HELP', 'AM_PM', 'TIME', 'DATE', 'ROUTE', 'FROM', 'AT'
)

t_ignore = ' \t'

# Define all keywords first
def t_BOOK(t):
    r'[Bb][Oo][Oo][Kk]'
    return t

def t_CONFIRM(t):
    r'[Cc][Oo][Nn][Ff][Ii][Rr][Mm]'
    return t

def t_PAY(t):
    r'[Pp][Aa][Yy]'
    return t

def t_CANCEL(t):
    r'[Cc][Aa][Nn][Cc][Ee][Ll]'
    return t

def t_LIST(t):
    r'[Ll][Ii][Ss][Tt]'
    return t

def t_HELP(t):
    r'[Hh][Ee][Ll][Pp]'
    return t

def t_TICKETS(t):
    r'[Tt][Ii][Cc][Kk][Ee][Tt][Ss]?'
    return t

def t_ON(t):
    r'[Oo][Nn]'
    return t

def t_TO(t):
    r'[Tt][Oo]'
    return t

def t_AT(t):
    r'[Aa][Tt]'
    return t

def t_FOR(t):
    r'[Ff][Oo][Rr]'
    return t

def t_FROM(t):
    r'[Ff][Rr][Oo][Mm]'
    return t

def t_ROUTE(t):
    r'[Rr][Oo][Uu][Tt][Ee]'
    return t

def t_SCHEDULE(t):
    r'[Ss][Cc][Hh][Ee][Dd][Uu][Ll][Ee]'
    return t

# Define special tokens for date, time, etc.
def t_DATE(t):
    r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}'
    return t

def t_AM_PM(t):
    r'(AM|PM|am|pm)'
    return t

def t_TIME(t):
    r'\d{1,2}:\d{2}'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_EVENT(t):
    r'(Reggae\s+Sumfest|Knutsford\s+Express|Rebel\s+Salute|Jamaica\s+Carnival|Dream\s+Weekend)'
    return t

def t_NAME(t):
    r'[A-Z][a-z]+(\s+[A-Z][a-z]+)*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()
