// ============================================================
//  control.v — Unidade de Controle Principal RISC-V32I
//
//  Sinais de saída:
//    RegWrite  — habilita escrita no banco de registradores
//    ALUSrcA   — 00=rs1  01=PC (auipc)  10=zero (lui)
//    ALUSrc    — 0=rs2   1=imediato
//    MemWrite  — habilita escrita na memória de dados
//    MemRead   — habilita leitura na memória de dados
//    ResultSrc — 00=ULA  01=Mem  10=PC+4
//    Branch    — instrução de desvio condicional
//    BranchNE  — 0=beq   1=bne
//    Jump      — jal (desvio incondicional)
//    JumpReg   — jalr
//    ALUOp     — 00=ADD forçado  01=SUB forçado  10=decodificar
// ============================================================
`timescale 1ns / 1ps

module control (
    input  wire [6:0] opcode,
    input  wire [2:0] funct3,

    output reg        RegWrite,
    output reg [1:0]  ALUSrcA,
    output reg        ALUSrc,
    output reg        MemWrite,
    output reg        MemRead,
    output reg [1:0]  ResultSrc,
    output reg        Branch,
    output reg        BranchNE,
    output reg        Jump,
    output reg        JumpReg,
    output reg [1:0]  ALUOp
);

    // Opcodes RISC-V32I
    localparam R_TYPE  = 7'b0110011; // add sub and or xor slt sll srl
    localparam I_ALU   = 7'b0010011; // addi andi ori xori slti slli srli
    localparam I_LOAD  = 7'b0000011; // lw lhu
    localparam S_TYPE  = 7'b0100011; // sw
    localparam B_TYPE  = 7'b1100011; // beq bne
    localparam J_JAL   = 7'b1101111; // jal
    localparam I_JALR  = 7'b1100111; // jalr
    localparam U_LUI   = 7'b0110111; // lui
    localparam U_AUIPC = 7'b0010111; // auipc

    always @(*) begin
        // ── valores padrão (NOP seguro) ──────────────────────
        RegWrite  = 1'b0;
        ALUSrcA   = 2'b00;
        ALUSrc    = 1'b0;
        MemWrite  = 1'b0;
        MemRead   = 1'b0;
        ResultSrc = 2'b00;
        Branch    = 1'b0;
        BranchNE  = 1'b0;
        Jump      = 1'b0;
        JumpReg   = 1'b0;
        ALUOp     = 2'b00;

        case (opcode)

            R_TYPE: begin
                // add, sub, and, or, xor, slt, sll, srl
                RegWrite = 1'b1;
                ALUOp    = 2'b10; // decodificar via funct3/funct7
            end

            I_ALU: begin
                // addi, andi, ori, xori, slti, slli, srli
                RegWrite = 1'b1;
                ALUSrc   = 1'b1;  // usa imediato como operando B
                ALUOp    = 2'b10; // decodificar via funct3
            end

            I_LOAD: begin
                // lw (funct3=010), lhu (funct3=101)
                RegWrite  = 1'b1;
                ALUSrc    = 1'b1;  // endereço = rs1 + imm
                MemRead   = 1'b1;
                ResultSrc = 2'b01; // escreve dado da memória em rd
                ALUOp     = 2'b00; // ADD para cálculo de endereço
            end

            S_TYPE: begin
                // sw
                ALUSrc   = 1'b1;  // endereço = rs1 + imm
                MemWrite = 1'b1;
                ALUOp    = 2'b00; // ADD para cálculo de endereço
            end

            B_TYPE: begin
                // beq (funct3=000), bne (funct3=001)
                Branch   = 1'b1;
                ALUOp    = 2'b01; // SUB: verifica igualdade via flag zero
                BranchNE = (funct3 == 3'b001) ? 1'b1 : 1'b0;
            end

            J_JAL: begin
                // jal: rd = PC+4,  PC = PC + imm_J
                RegWrite  = 1'b1;
                ResultSrc = 2'b10; // PC+4 gravado em rd
                Jump      = 1'b1;
                // ALUOp=00 (padrão) — ALU não é usada para destino aqui
            end

            I_JALR: begin
                // jalr: rd = PC+4,  PC = (rs1 + imm) & ~1
                RegWrite  = 1'b1;
                ALUSrc    = 1'b1;  // destino = rs1 + imm (calculado pela ULA)
                ResultSrc = 2'b10; // PC+4 gravado em rd
                JumpReg   = 1'b1;
                ALUOp     = 2'b00; // ADD
            end

            U_LUI: begin
                // lui: rd = {imm[31:12], 12'b0}
                RegWrite = 1'b1;
                ALUSrcA  = 2'b10; // A = 0 (forçado)
                ALUSrc   = 1'b1;  // B = imm
                ALUOp    = 2'b00; // ADD: 0 + imm = imm
            end

            U_AUIPC: begin
                // auipc: rd = PC + {imm[31:12], 12'b0}
                RegWrite = 1'b1;
                ALUSrcA  = 2'b01; // A = PC
                ALUSrc   = 1'b1;  // B = imm
                ALUOp    = 2'b00; // ADD: PC + imm
            end

            default: ; // NOP — mantém padrão

        endcase
    end

endmodule
