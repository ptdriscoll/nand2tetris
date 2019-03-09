// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//i = SCREEN
//screenend = 24575

//LOOP:
//if KBD = 0 goto WHITE
//color = -1

//WHITE:
//color = 0

//SCREENLOOP:
//if i > screenend goto LOOP

//RAM[i] = color
//i = i + 16
//goto SCREENLOOP

/////////////////////////////////

//set screen end variable
@24575
D=A
@screenend
M=D

(LOOP)
//set index variable
@SCREEN
D=A
@i 
M=D

//set color to white as default 
@color
M=0

//check if any key is down, if not then skip setting color to black 
@KBD
D=M
@SCREELOOP
D;JEQ

//set color to black if key pressed
@color
M=-1

//loop through screen registers and set to color
(SCREENLOOP)

//break loop after all screen pixels set
@i
D=M
@screenend
D=D-M
@LOOP
D;JGT

//set next screen register to color
@color
D=M
@i
A=M
M=D

//set next screen register in loop
@i
M=M+1

@SCREENLOOP
0;JMP