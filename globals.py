PROMPT = 'PG > '


enum_value = 0
def enum(reflow=False):
    global enum_value
    if reflow:
        enum_value = 0
    enum_value += 1
    return enum_value - 1


# Operations
PRNT  = enum(reflow=True)
EXIT  = enum()
