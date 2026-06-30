// ============================================================
//  imm_gen.v — Gerador de Imediato RISC-V32I
//
//  Formato  | Instrução          | Extensão de sinal
//  I-type   | addi/lw/jalr/etc.  | 12 bits → 32
//  S-type   | sw                 | 12 bits → 32
//  B-type   | beq/bne            | 13 bits → 32 (bit 0 = 0)
//  U-type   | lui/auipc          | 20 bits em [31:12]
//  J-type   | jal                | 21 bits → 32 (bit 0 = 0)
// ============================================================
`timescale 1ns / 1ps

module imm_gen (
    input  wire [31:0] instruction,
    output reg  [31:0] imm
);

    wire [6:0] opcode = instruction[6:0];

    always @(*) begin
        case (opcode)

            // ── I-type ──────────────────────────────────────
            // addi, andi, ori, xori, slti, slli, srli
            7'b0010011,
            // lw, lhu
            7'b0000011,
            // jalr
            7'b1100111:
                imm = {{20{instruction[31]}},
                         instruction[31:20]};

            // ── S-type ──────────────────────────────────────
            // sw
            7'b0100011:
                imm = {{20{instruction[31]}},
                         instruction[31:25],
                         instruction[11:7]};

            // ── B-type ──────────────────────────────────────
            // beq, bne
            // imm[12|10:5] em inst[31:25], imm[4:1|11] em inst[11:7]
            7'b1100011:
                imm = {{19{instruction[31]}},
                         instruction[31],    // imm[12]
                         instruction[7],     // imm[11]
                         instruction[30:25], // imm[10:5]
                         instruction[11:8],  // imm[4:1]
                         1'b0};              // imm[0] = 0

            // ── U-type ──────────────────────────────────────
            // lui, auipc
            7'b0110111,
            7'b0010111:
                imm = {instruction[31:12], 12'b0};

            // ── J-type ──────────────────────────────────────
            // jal
            // imm[20|10:1|11|19:12] espalhados na instrução
            7'b1101111:
                imm = {{11{instruction[31]}},
                         instruction[31],    // imm[20]
                         instruction[19:12], // imm[19:12]
                         instruction[20],    // imm[11]
                         instruction[30:21], // imm[10:1]
                         1'b0};              // imm[0] = 0

            default: imm = 32'd0;

        endcase
    end

endmodule
