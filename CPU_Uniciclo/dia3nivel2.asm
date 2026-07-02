.data
A:.word 1,2,3,4
B:.word 5,6,7,8
C:.word 0,0,0,0
.text
main:
lui s0,0x10010
addi s0,s0,0
lui s1,0x10010
addi s1,s1,16
lui s2,0x10010
addi s2,s2,32
addi t0,x0,4
L: beq t0,x0,E
lw t1,0(s0)
lw t2,0(s1)
add t3,t1,t2
sw t3,0(s2)
addi s0,s0,4
addi s1,s1,4
addi s2,s2,4
addi t0,t0,-1
jal x0,L
E: jalr x0,0(ra)
