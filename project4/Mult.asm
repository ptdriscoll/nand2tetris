// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

//i = R0
//sum = 0

//LOOP:
//if i = 0 goto STOP
//sum = sum + R1  
//i = i - 1
//goto LOOP

//STOP:
//R2 = sum   
//END

@R0
D=M

@i
M=D

@sum
M=0

(LOOP)
@i
D=M
@STOP
D;JEQ

@sum
D=M
@R1
D=D+M
@sum
M=D

@i
M=M-1

@LOOP
0;JMP

(STOP)
@sum
D=M
@R2
M=D

(END)
@END
0;JMP