.data

BUFFER:
    .half 0x1234
    .half 0xABCD
    .half 0x0F0F
    .half 0xAAAA
    .half 0x5555
    .half 0x1357
    .half 0x2468
    .half 0xFFFF

CRC_OUT:
    .word 0

.text

main:

    lui  s0, 65552
    addi s0, s0, 0

    # crc inicial
    addi s1, x0, 0

    # contador
    addi s2, x0, 8

MAIN_LOOP:

    lhu  t0, 0(s0)

    xor  s1, s1, t0

    addi s3, x0, 16

BIT_LOOP:

    andi t1, s1, 1

    beq  t1, x0, SHIFT_ONLY

    addi t2, x0, 0x39
    xor  s1, s1, t2

SHIFT_ONLY:

    srl  s1, s1, s1

    addi s3, s3, -1

    bne  s3, x0, BIT_LOOP

    addi s0, s0, 2

    addi s2, s2, -1

    bne  s2, x0, MAIN_LOOP

    lui  t3, 65552
    addi t3, t3, 16

    sw   s1, 0(t3)

END:
    jal  x0, END