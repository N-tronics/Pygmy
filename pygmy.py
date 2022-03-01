# Pygmy - A general purpose programming language
import sys
import globals as gb
import subprocess

# Sample test program
data = [
    ('hw', 'Hello, World!', 13),
    ('num', 12, 1)
]

program = [
    (gb.PRNTLN, 'hw'),
    (gb.PRNTLN, 'num'),
    (gb.EXIT, 0)
]


def simulate_file(filepath):
    # with open(filepath, 'r') as f:
    #    code = f.readlines()
    for instr in program:
        if instr[0] == gb.PRNT:
            addr = tuple(filter(lambda x: x[0] == instr[1], data))
            if not addr:
                print("Symbol %s not defined." % instr[1])
                sys.exit(1)
            addr = addr[0]
            if isinstance(addr[1], int):
                print(addr[1])
            else:
                for i in range(addr[2]):
                    if addr[1][i] == '\0':
                        break
                    print(addr[1][i], end='')
            # print(tuple(filter(lambda x: x[0] == instr[1], data))[0][1], end='')
        elif instr[0] == gb.EXIT:
            sys.exit(instr[1])


def compile_file(filepath):
    # with open(filepath, 'r') as f:
    #    code = f.readlines()
    # Basename of file. Eg: first.pg -> first
    basename = filepath.split('.')[0]
    asm_file = open('%s.asm' % basename, "w")

    # Include files
    asm_file.write('%include \'stdlib.asm\'\n\n')

    # Write the data section
    asm_file.write("section .data\n")
    for var in data:
        asm_file.write("%s db " % var[0])
        if isinstance(var[1], int):
            asm_file.write(f'{var[1]}')
        else:
            asm_file.write('\'')
            add_comma = False
            for char in range(var[2]):
                if var[1][char] == '\n':
                    asm_file.write("', 0ah")
                    add_comma = True
                elif var[1][char] == '\0':
                    asm_file.write("', 0")
                    break
                else:
                    if add_comma: asm_file.write(', \'')
                    asm_file.write('%c' % var[1][char])
            else:
                asm_file.write('\'')
        asm_file.write('\n')
    asm_file.write('\n')

    # Write the text section
    asm_file.write('section .text\n')
    asm_file.write('global _start\n')
    asm_file.write('_start:\n')

    for instr in program:
        if instr[0] == gb.PRNT or instr[0] == gb.PRNTLN:
            addr = tuple(filter(lambda x: x[0] == instr[1], data))
            if not addr:
                print("Invalid symbol %s" % instr[1])
                sys.exit(1)
            if isinstance(addr[0][1], int):
                asm_file.write(f'    movzx rax, byte [{addr[0][0]}]\n')
            else:
                asm_file.write(f'    mov rax, {addr[0][0]}\n')
            asm_file.write(f'    mov rdi, {addr[0][2]}\n')
            if isinstance(addr[0][1], int):
                asm_file.write('    call prnti\n')
            else:
                asm_file.write('    call prnts\n')
            if instr[0] == gb.PRNTLN: asm_file.write('    call prntlf\n')
        elif instr[0] == gb.EXIT:
            asm_file.write(f'    mov rdi, {instr[1]}\n')
            asm_file.write( '    call exit\n')
    
    asm_file.close()

    # Run the compilation script to compile and link asm file
    subprocess.run(['./asm64.sh', basename])

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
