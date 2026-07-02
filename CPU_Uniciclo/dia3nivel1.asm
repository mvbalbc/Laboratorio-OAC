.data
N:.word 8
V:.word 4,7,1,9,2,8,3,6
OUT:.word 0,0,0,0,0,0,0,0
.text
main:
lui s0,0x10010
addi s0,s0,0
lw s1,0(s0)
lui s2,0x10010
addi s2,s2,4
lui s3,0x10010
addi s3,s3,36
addi t0,x0,0
addi t4,x0,1
L: beq t0,s1,E
lw t1,0(s2)
sll t1,t1,t4
xori t1,t1,15
sw t1,0(s3)
addi s2,s2,4
addi s3,s3,4
addi t0,t0,1
jal x0,L
E: jalr x0,0(ra)