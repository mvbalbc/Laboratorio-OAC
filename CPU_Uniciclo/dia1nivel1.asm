.data
n:      .word 8
array:  .word 3,1,4,1,5,9,2,6
result: .word 0

.text
main:

    lui   t0, 0x10010
    addi  t0, t0, 0
    lw    t1, 0(t0)

    lui   t2, 0x10010
    addi  t2, t2, 4

    addi  t3, x0, 0
    addi  t4, x0, 0

loop:
    beq   t4, t1, done

    lw    t5, 0(t2)
    add   t3, t3, t5

    addi  t2, t2, 4
    addi  t4, t4, 1

    jal   x0, loop

done:

    lui   t6, 0x10010
    addi  t6, t6, 36

    sw    t3, 0(t6)

    jalr  x0, 0(ra)