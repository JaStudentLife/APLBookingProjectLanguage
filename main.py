from parser import parser

while True:
    try:
        command = input(">> ").strip()
    except EOFError:
        break
    if not command:
        continue

    parser.parse(command)
