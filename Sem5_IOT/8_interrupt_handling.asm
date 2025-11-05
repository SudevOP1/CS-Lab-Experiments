DATA SEGMENT
    msg1 DB 'Enter a character: $'
    msg2 DB 0AH,0DH, 'You entered: $'
DATA ENDS

CODE SEGMENT
ASSUME CS:CODE, DS:DATA

START:
    MOV AX, DATA
    MOV DS, AX ; Initialize data segment
    
    ; Display first message
    LEA DX, msg1
    MOV AH, 09H
    INT 21H ; DOS interrupt to print string
    
    ; Read a character
    MOV AH, 01H
    INT 21H ; Read char from keyboard
    MOV BL, AL ; Store the input character in BL
    
    ; Display second message
    LEA DX, msg2
    MOV AH, 09H
    INT 21H
    
    ; Display the entered character
    MOV DL, BL
    MOV AH, 02H
    INT 21H ; Display the character
    
    ; Exit program
    MOV AH, 4CH
    INT 21H
CODE
ENDS END
START