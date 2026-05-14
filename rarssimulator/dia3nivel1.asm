.data
VET:    .word 2, 5, 8, 12, 15, 21, 30, 42
	.word 56, 63, 71, 84, 95, 101, 120, 150

TARGET:	.word 84

RESULT:	.word -1

.text
    lui  s0, 65552
    addi s0, s0, 0
    lui  s1, 65552
    addi s1, s1, 64
    lw   s2, 0(s1)

    addi s3, x0, 0

    addi s4, x0, 15

LOOP:
    slt  t0, s4, s3
    bne  t0, x0, END_NOT_FOUND
    add  t1, s3, s4
    srl  t1, t1, t1

    # offset = mid * 4
    sll  t2, t1, t2
    add  t3, s0, t2
    lw   t4, 0(t3)

    beq  t4, s2, FOUND

    slt  t5, t4, s2
    bne  t5, x0, GO_RIGHT

GO_LEFT:

    addi s4, t1, -1
    bne  x0, x0, LOOP

GO_RIGHT:

    addi s3, t1, 1
    bne  x0, x0, LOOP

FOUND:

    lui  t6, 65552
    addi t6, t6, 68

    sw   t1, 0(t6)

END:
    jal  x0, END
    
END_NOT_FOUND:
    lui  t6, 65552
    addi t6, t6, 68
    addi t0, x0, -1
    sw   t0, 0(t6)
    jal  x0, END