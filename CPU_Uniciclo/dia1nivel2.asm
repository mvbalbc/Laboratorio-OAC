.data
n:       .word 10
limit:   .word 50
array:   .word 12,55,88,10,51,49,50,100,3,75
count:   .word 0

.text
main:

    lui   s0, 0x10010
    addi  s0, s0, 0
    lw    s1, 0(s0)

    lui   s2, 0x10010
    addi  s2, s2, 4
    lw    s3, 0(s2)

    lui   s4, 0x10010
    addi  s4, s4, 8

    addi  s5, x0, 0
    addi  s6, x0, 0

loop:
    beq   s6, s1, finish

    lw    t0, 0(s4)

    slt   t1, s3, t0
    beq   t1, x0, skip

    addi  s5, s5, 1

skip:

    addi  s4, s4, 4
    addi  s6, s6, 1

    jal   x0, loop

finish:

    lui   t2, 0x10010
    addi  t2, t2, 48

    sw    s5, 0(t2)

    jalr  x0, 0(ra)