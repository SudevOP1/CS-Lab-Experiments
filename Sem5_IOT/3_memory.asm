.MODEL SMALL
.STACK 100h


.DATA
    ; Task 1 - Basic Memory Access
    num1 DB 5
    num2 DB 10
    result1 DB ?

    ; Task 2 - Stack-Based Memory Access
    num3 DB 6
    num4 DB 4
    result2 DB ?

    ; Task 3 - Simulated Dynamic Memory Allocation
    result3 DB ?


.CODE
MAIN PROC
    ; Set up data segment
    MOV AX, @DATA
    MOV DS, AX

    ; Task 1: Add num1 + num2 → result1
    MOV AL, num1
    MOV BL, num2
    ADD AL, BL
    MOV result1, AL
    
    ; Task 2: Use stack for num3, num4 addition - result2
    XOR AH, AH
    MOV AL, num3
    PUSH AX
    MOV AL, num4
    PUSH AX
    POP BX ; BX = num4
    POP AX ; AX = num3
    ADD AL, BL B AL = num3 + num4
    MOV result2, AL
    
    ; Task 3: Simulated allocation - result3 = 20
    MOV AL, 20
    MOV result3, AL
    
    ; Exit to DOS
    MOV AH, 4Ch
    INT 21h
MAIN ENDP
END MAIN
