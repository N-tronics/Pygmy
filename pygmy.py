# Pygmy - A general purpose programming language
import sys
import globals as gb

data = [
    ('hw', 'Hello, World!\n\0', 15)
]

program = [
    (gb.PRNT, 'hw'),
    (gb.EXIT, 0)
]


def simulate_file(filepath):
    with open(filepath, 'r') as f:
        code = f.readlines()
    for instr in program:
        if instr[0] == gb.PRNT:
            addr = tuple(filter(lambda x: x[0] == instr[1], data))
            if addr == ():
                print("Variable %s not defined." % instr[1])
                sys.exit(1)
            addr = addr[0]
            for i in range(addr[2]):
                if addr[1][i] == '\0':
                    break
                print(addr[1][i], end='')
            # print(tuple(filter(lambda x: x[0] == instr[1], data))[0][1], end='')
        elif instr[0] == gb.EXIT:
            sys.exit(instr[1])


def compile_file(filepath):
    with open(filepath, 'r') as f:
        code = f.readlines()
    asm_file = open("%s.asm" % filepath.split('.')[0], "w")
    asm_file.write("section .data\n")
    for var in data:
        asm_file.write("%s db '" % var[0])
        for char in range(var[2]):
            if var[1][char] == '\\':
                char += 1
                if var[1][char] == 'n':
                    asm_file.write("', 0ah, '")
                elif var[1][char] == '0':
                    asm_file.write("', 0h, '")
            asm_file.write('%c' % var[1][char])
        asm_file.write('\'\n')
    asm_file.close()

def launch_shell():
    cmd = input(gb.PROMPT)
    while cmd != 'exit':
        print(cmd)
        cmd = input(gb.PROMPT)
    print('Bye.')


def print_help():
    print("\033[33mUsage\033[m: pygmy.py [subcommand] [file?]")
    print("       pygmy.py sim [file]     Simulates the file given")
    print("       pygmy.py com [file]     Compiles the file given")
    print("       pygmy.py shl            Launches an interactive shell")
    print("       pygmy.py help           Prints the message")


if __name__ == '__main__':
    # Check for subcommands
    argv = sys.argv[1:]
    if argv[0] == 'sim' and len(argv) >= 2:
        argv = argv[1:]
        simulate_file(argv[0])
    elif argv[0] == 'com' and len(argv) >= 2:
        argv = argv[1:]
        compile_file(argv[0])
    elif argv[0] == 'shl':
        launch_shell()
        pass
    elif argv[0] == 'help':
        print_help()
    else:
        print_help()
        print("\n\033[31mERROR\033[m: Invalid subcommand")
