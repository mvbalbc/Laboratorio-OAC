// ============================================================
//  alu.v — Unidade Lógico-Aritmética 32 bits
//
//  alu_op | Operação
//  0000   | ADD  — a + b
//  0001   | SUB  — a - b
//  0010   | AND  — a & b
//  0011   | OR   — a | b
//  0100   | XOR  — a ^ b
//  0101   | SLT  — (signed a < signed b) ? 1 : 0
//  0110   | SLL  — a << b[4:0]
//  0111   | SRL  — a >> b[4:0]  (lógico)
//  1000   | SRA  — a >>> b[4:0] (aritmético)
//
//  zero   — asserted quando result == 0 (usado por branch)
// ============================================================
`timescale 1ns / 1ps

module alu (
    input  wire [31:0] a,
    input  wire [31:0] b,
    input  wire [3:0]  alu_op,
    output reg  [31:0] result,
    output wire        zero
);

    always @(*) begin
        case (alu_op)
            4'b0000: result = a + b;
            4'b0001: result = a - b;
            4'b0010: result = a & b;
            4'b0011: result = a | b;
            4'b0100: result = a ^ b;
            4'b0101: result = ($signed(a) < $signed(b)) ? 32'd1 : 32'd0;
            4'b0110: result = a << b[4:0];
            4'b0111: result = a >> b[4:0];
            4'b1000: result = $signed(a) >>> b[4:0];
            default: result = 32'd0;
        endcase
    end

    assign zero = (result == 32'd0);

endmodule
