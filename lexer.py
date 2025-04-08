import ply.lex as lex

tokens = (
    'BOOK', 'CONFIRM', 'PAY', 'CANCEL', 'LIST',
    'NUMBER', 'TICKETS', 'TO', 'ON', 'DATE',
    'FOR', 'NAME', 'SCHEDULE', 'HELP', 'AM_PM', 'TIME', 'COMMA', 'COLON', 'ROUTE', 'FROM', 'AT'
)

t_ignore = ' \t'

def t_AT(t):
    r'at'
    return t

def t_BOOK(t):
    r'[Bb]ook'
    return t

def t_HELP(t):
    r'[Hh]elp'
    return t

def t_CONFIRM(t):
    r'[Cc]onfirm'
    return t

def t_PAY(t):
    r'[Pp]ay'
    return t

def t_CANCEL(t):
    r'[Cc]ancel'
    return t

def t_LIST(t):
    r'[Ll]ist'
    return t

def t_TICKETS(t):
    r'tickets?'
    return t

def t_TO(t):
    r'to'
    return t

def t_ON(t):
    r'on'
    return t

def t_FOR(t):
    r'for'
    return t

def t_SCHEDULE(t):
    r'schedule'
    return t

def t_ROUTE(t):
    r'[Rr]oute'
    return t

def t_FROM(t):
    r'[Ff]rom'
    return t

def t_DATE(t):
    r'(January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},?\s?\d{0,4}'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_TIME(t):
    r'\d{1,2}:\d{2}\s?(AM|PM|am|pm)'
    return t

def t_COMMA(t):
    r','
    return t

def t_COLON(t):
    r':'
    return t

def t_NAME(t):
    r'[A-Z][a-z]+(\s[A-Z][a-z]+)*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()
