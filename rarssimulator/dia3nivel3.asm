.data

BITS:
    .word 1,0,1,1,0,1,1,1,0,0,1,0,1,1,0,1

FOUND:
    .word 0

.text


    # base sequência
    lui  s0, 65552
    addi s0, s0, 0

    # contador
    addi s1, x0, 16

    # estado atual
    addi s2, x0, 0

MAIN_LOOP:

    beq  s1, x0, END

    lw   t0, 0(s0)

STATE0:

    bne  s2, x0, STATE1_CHECK

    addi t1, x0, 1

    bne  t0, t1, NEXT

    addi s2, x0, 1

    bne  x0, x0, NEXT

STATE1_CHECK:

    addi t1, x0, 1
    bne  s2, t1, STATE2_CHECK

    beq  t0, x0, S1_OK

    addi s2, x0, 1
    bne  x0, x0, NEXT

S1_OK:

    addi s2, x0, 2
    bne  x0, x0, NEXT

STATE2_CHECK:

    addi t1, x0, 2
    bne  s2, t1, STATE3_CHECK

    addi t2, x0, 1

    beq  t0, t2, S2_OK

    addi s2, x0, 0
    bne  x0, x0, NEXT

S2_OK:

    addi s2, x0, 3
    bne  x0, x0, NEXT

STATE3_CHECK:

    addi t1, x0, 3
    bne  s2, t1, STATE4_CHECK

    addi t2, x0, 1

    beq  t0, t2, S3_OK

    addi s2, x0, 0
    bne  x0, x0, NEXT

S3_OK:

    addi s2, x0, 4
    bne  x0, x0, NEXT

STATE4_CHECK:

    addi t1, x0, 4
    bne  s2, t1, STATE5_CHECK

    beq  t0, x0, S4_OK

    addi s2, x0, 1
    bne  x0, x0, NEXT

S4_OK:

    addi s2, x0, 5
    bne  x0, x0, NEXT

STATE5_CHECK:

    addi t1, x0, 5
    bne  s2, t1, NEXT

    addi t2, x0, 1

    beq  t0, t2, DETECTED

    addi s2, x0, 0
    bne  x0, x0, NEXT

DETECTED:

    lui  t3, 65552
    addi t3, t3, 64

    addi t4, x0, 1

    sw   t4, 0(t3)

    jal  x0, END

NEXT:

    addi s0, s0, 4
    addi s1, s1, -1

    bne  x0, x0, MAIN_LOOP

END:
    jal  x0, END