prnti:
    push rbx
    push rcx
    push rdx
    push rsi
    ; RCX counts the number of digits in the number
    ; Counts up when converting digits to ASCII and down when printing
    mov rcx, 0
    ; RSI is the divisor
    mov rsi, 10
.div_loop:
    inc rcx
    ; Clear RDX as RDX:RAX is taken is the dividend
    mov rdx, 0
    idiv rsi
    ; Convert remainder (i.e digit of number) to ASCII value
    add rdx, 48
    ; Digits are pushed on the stack and then popped when writing
    push rdx
    ; If the quotient is 0, then we have gone through the entire number
    cmp rax, 0
    jnz .div_loop
.prnt_loop:
    dec rcx
    ; Since write syscall takes a pointer to a character, we use the current stack pointer
    mov rax, rsp
    mov rdi, 1
    ; Save RCX as it get modified somehow
    push rcx
    call prnts
    ; Pop RCX from the stack
    pop rcx
    ; Pop the printed digit from the stack
    pop rax
    ; If RCX is 0, then we have printed all digits
    cmp rcx, 0
    jnz .prnt_loop
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    ret

prnts:
    ; RAX holds the syscall number, RDI holds the file descriptor, RSI holds the character pointer
    ; and RDX holds the number of characters to print
    mov rsi, rax
    mov rdx, rdi
    mov rdi, 1
    mov rax, 1
    syscall
    ret

prntlf:
    push rax
    push rdi
    push rsi
    push rdx
    ; Push a new line character (0xa) to stack
    mov rax, 0ah
    push rax
    ; Use the stack pointer as the address to the character
    mov rax, rsp
    mov rdi, 1
    call prnts
    pop rax
    pop rdx
    pop rsi
    pop rdi
    pop rax
    ret
    

exit:
    mov rax, 3ch
    syscall