.data
A: .word 1,2,3,4
B: .word 5,6,7,8
C: .word 0,0,0,0

.text
main:

    lui   s0, 0x10010
    addi  s0, s0, 0

    lui   s1, 0x10010
    addi  s1, s1, 16

    lui   s2, 0x10010
    addi  s2, s2, 32

    # C00

    lw    a0, 0(s0)
    lw    a1, 0(s1)
    jal   ra, mult

    addi  t0, a0, 0

    lw    a0, 4(s0)
    lw    a1, 8(s1)
    jal   ra, mult

    add   t0, t0, a0
    sw    t0, 0(s2)

    # C01

    lw    a0, 0(s0)
    lw    a1, 4(s1)
    jal   ra, mult

    addi  t0, a0, 0

    lw    a0, 4(s0)
    lw    a1, 12(s1)
    jal   ra, mult

    add   t0, t0, a0
    sw    t0, 4(s2)

    # C10

    lw    a0, 8(s0)
    lw    a1, 0(s1)
    jal   ra, mult

    addi  t0, a0, 0

    lw    a0, 12(s0)
    lw    a1, 8(s1)
    jal   ra, mult

    add   t0, t0, a0
    sw    t0, 8(s2)

    # C11

    lw    a0, 8(s0)
    lw    a1, 4(s1)
    jal   ra, mult

    addi  t0, a0, 0

    lw    a0, 12(s0)
    lw    a1, 12(s1)
    jal   ra, mult

    add   t0, t0, a0
    sw    t0, 12(s2)

    jalr  x0, 0(ra)

mult:

    addi  t1, x0, 0
    addi  t2, x0, 0

mloop:

    beq   t2, a1, mend

    add   t1, t1, a0

    addi  t2, t2, 1

    jal   x0, mloop

mend:

    addi  a0, t1, 0

    jalr  x0, 0(ra)