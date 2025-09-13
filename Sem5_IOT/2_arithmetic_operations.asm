.MODEL SMALL
.STACK 100h
.DATA
    num1 DB 10h
    num2 DB 04h
    result DB ?
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    MOV AL, num1
    ADD AL, num2
    MOV result, AL

    MOV AL, num1
    SUB AL, num2
    MOV result, AL

    MOV AL, num1
    MUL BL, num2
    MUL BL
    MOV result, AL

    MOV AL, num1
    MOV BL, num2
    DIV BL
    MOV result, AL

    MOV AH, 4Ch
    INT 21h
MAIN ENDP
END MAIN

