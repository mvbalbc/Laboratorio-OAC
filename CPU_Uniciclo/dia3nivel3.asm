.data
N:.word 8
BUF:.word 10,20,30,40,50,60,70,80
.text
main:
lui s0,0x10010
addi s0,s0,0
lw s1,0(s0)
lui s2,0x10010
addi s2,s2,4
addi t0,x0,0
addi t5,x0,1
L: beq t0,s1,E
lw t1,0(s2)
xor t1,t1,t0
or t1,t1,t5
and t1,t1,t1
srl t2,t1,t5
add t1,t1,t2
sw t1,0(s2)
addi s2,s2,4
addi t0,t0,1
jal x0,L
E: jalr x0,0(ra)
