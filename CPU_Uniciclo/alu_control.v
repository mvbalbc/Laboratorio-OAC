// ============================================================
//  alu_control.v — Controle da ULA RISC-V32I
//
//  ALUOp | Ação
//  00    | ADD forçado (loads, stores, JAL, JALR, LUI, AUIPC)
//  01    | SUB forçado (branches — compara rs1-rs2)
//  10    | Decodifica via funct3/funct7
//
//  alu_op interno:
//  0000 ADD | 0001 SUB | 0010 AND | 0011 OR
//  0100 XOR | 0101 SLT | 0110 SLL | 0111 SRL | 1000 SRA
// ============================================================
`timescale 1ns / 1ps

module alu_control (
    input  wire [1:0] ALUOp,
    input  wire [2:0] funct3,
    input  wire [6:0] funct7,
    input  wire       itype,   // 1 = I-type ALU (0010011): suprime detecção de SUB
    output reg  [3:0] alu_op
);

    localparam ALU_ADD = 4'b0000;
    localparam ALU_SUB = 4'b0001;
    localparam ALU_AND = 4'b0010;
    localparam ALU_OR  = 4'b0011;
    localparam ALU_XOR = 4'b0100;
    localparam ALU_SLT = 4'b0101;
    localparam ALU_SLL = 4'b0110;
    localparam ALU_SRL = 4'b0111;
    localparam ALU_SRA = 4'b1000;

    always @(*) begin
        // Fail-safe: default antes do case impede latch no Quartus
        alu_op = ALU_ADD;

        case (ALUOp)

            2'b00: alu_op = ALU_ADD; // ADD forçado

            2'b01: alu_op = ALU_SUB; // SUB forçado (branch)

            2'b10: begin             // decodificar funct3 / funct7
                case (funct3)
                    // funct3=000: ADD ou SUB
                    // SUB apenas em R-type quando funct7[5]=1
                    // (~itype garante que addi nunca vira SUB)
                    3'b000: alu_op = (funct7[5] & ~itype) ? ALU_SUB : ALU_ADD;
                    3'b111: alu_op = ALU_AND; // and / andi
                    3'b110: alu_op = ALU_OR;  // or  / ori
                    3'b100: alu_op = ALU_XOR; // xor / xori
                    3'b010: alu_op = ALU_SLT; // slt / slti (signed)
                    3'b001: alu_op = ALU_SLL; // sll / slli
                    3'b101: alu_op = funct7[5] ? ALU_SRA : ALU_SRL;
                    default: alu_op = ALU_ADD;
                endcase
            end

            default: alu_op = ALU_ADD;

        endcase
    end

endmodule
