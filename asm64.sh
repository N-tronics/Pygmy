#!/bin/bash
# Simple assemble and link script

if [ -z $1 ]; then
	echo "Usage: ./asm64 <asmMainFile>(no extension)"
	exit 1
fi

if [ ! -e "$1.asm" ]; then
	echo "Error: $1.asm not found."
	echo "Note: do not enter file extensions."
	exit 1
fi

mkdir -p $1
nasm -f elf64 $1.asm -l $1/$1.lst -o $1/$1.o -F dwarf -g
ld -g -o $1/$1 $1/$1.o
echo -e "\033[32mSuccessfully built $1/$1.\033[m"
