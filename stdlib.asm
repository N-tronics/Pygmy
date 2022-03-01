prnt:
    push rsi
    push rdx
    mov rsi, rax
    mov rdx, rdi
    mov rdi, 1
    mov rax, 1
    syscall
    pop rdx
    pop rsi
    ret