// ============================================================
//  riscv_top.v — Unidade Operativa Uniciclo RISC-V32I
//  Disciplina: OAC – UnB, 1o/2026
//  Arquitetura Harvard, clock único, sem pipeline
// ============================================================
`timescale 1ns / 1ps

module riscv_top (
    input  wire        clk,
    input  wire        rst,

    // Portas de saída para observação no VWF (Virtual Pins)
    output wire [31:0] dbg_pc,
    output wire [31:0] dbg_instr,
    output wire [31:0] dbg_alu_result,
    output wire [31:0] dbg_mem_rdata,
    output wire [31:0] dbg_mem_wdata,
    output wire [31:0] dbg_mem_addr,
    output wire [31:0] dbg_wr_data,
    output wire [31:0] dbg_rs1_data,
    output wire [31:0] dbg_rs2_data,
    output wire [31:0] dbg_imm,
    output wire        dbg_RegWrite,
    output wire        dbg_MemWrite,
    output wire        dbg_MemRead,
    output wire        dbg_Branch,
    output wire        dbg_Jump,
    output wire        dbg_JumpReg,
    output wire [1:0]  dbg_ALUOp,
    output wire [1:0]  dbg_ResultSrc,
    output wire [3:0]  dbg_alu_ctrl_op,
    output wire        dbg_zero,
    output wire        dbg_branch_taken
);

    // ============================================================
    // PC — inicia em TEXT_BASE = 0x00400000
    // ============================================================
    reg  [31:0] pc;
    wire [31:0] pc_next;
    wire [31:0] pc_plus4;

    initial pc = 32'h0040_0000;

    always @(posedge clk or posedge rst)
        pc <= rst ? 32'h0040_0000 : pc_next;

    assign pc_plus4 = pc + 32'd4;

    // ============================================================
    // Memória de Instruções (Harvard — somente leitura)
    // ============================================================
    wire [31:0] instruction;
    inst_mem u_imem (
        .clk   (clk),
        .addr  (pc),
        .rdata (instruction)
    );

    // ============================================================
    // Decodificação dos campos da instrução
    // ============================================================
    wire [6:0] opcode = instruction[6:0];
    wire [4:0] rd     = instruction[11:7];
    wire [2:0] funct3 = instruction[14:12];
    wire [4:0] rs1    = instruction[19:15];
    wire [4:0] rs2    = instruction[24:20];
    wire [6:0] funct7 = instruction[31:25];

    // ============================================================
    // Unidade de Controle Principal
    // ============================================================
    wire        RegWrite, ALUSrc, MemWrite, MemRead;
    wire        Branch,   BranchNE, Jump, JumpReg;
    wire [1:0]  ALUSrcA, ResultSrc, ALUOp;

    control u_ctrl (
        .opcode    (opcode),
        .funct3    (funct3),
        .RegWrite  (RegWrite),
        .ALUSrcA   (ALUSrcA),
        .ALUSrc    (ALUSrc),
        .MemWrite  (MemWrite),
        .MemRead   (MemRead),
        .ResultSrc (ResultSrc),
        .Branch    (Branch),
        .BranchNE  (BranchNE),
        .Jump      (Jump),
        .JumpReg   (JumpReg),
        .ALUOp     (ALUOp)
    );

    // ============================================================
    // Banco de Registradores
    // ============================================================
    wire [31:0] rs1_data, rs2_data, wr_data;
    wire [31:0] dbg_x0,  dbg_x1,  dbg_x2,  dbg_x3,
                dbg_x4,  dbg_x5,  dbg_x6,  dbg_x7,
                dbg_x8,  dbg_x9,  dbg_x10, dbg_x11,
                dbg_x12, dbg_x13, dbg_x14, dbg_x15,
                dbg_x16, dbg_x17, dbg_x18, dbg_x19,
                dbg_x20, dbg_x21, dbg_x22, dbg_x23,
                dbg_x24, dbg_x25, dbg_x26, dbg_x27,
                dbg_x28, dbg_x29, dbg_x30, dbg_x31;

    reg_file u_rf (
        .clk      (clk),
        .RegWrite (RegWrite),
        .rs1      (rs1),      .rs2     (rs2),
        .rd       (rd),       .wr_data (wr_data),
        .rs1_data (rs1_data), .rs2_data(rs2_data),
        .dbg_x0 (dbg_x0),  .dbg_x1 (dbg_x1),  .dbg_x2 (dbg_x2),  .dbg_x3 (dbg_x3),
        .dbg_x4 (dbg_x4),  .dbg_x5 (dbg_x5),  .dbg_x6 (dbg_x6),  .dbg_x7 (dbg_x7),
        .dbg_x8 (dbg_x8),  .dbg_x9 (dbg_x9),  .dbg_x10(dbg_x10), .dbg_x11(dbg_x11),
        .dbg_x12(dbg_x12), .dbg_x13(dbg_x13), .dbg_x14(dbg_x14), .dbg_x15(dbg_x15),
        .dbg_x16(dbg_x16), .dbg_x17(dbg_x17), .dbg_x18(dbg_x18), .dbg_x19(dbg_x19),
        .dbg_x20(dbg_x20), .dbg_x21(dbg_x21), .dbg_x22(dbg_x22), .dbg_x23(dbg_x23),
        .dbg_x24(dbg_x24), .dbg_x25(dbg_x25), .dbg_x26(dbg_x26), .dbg_x27(dbg_x27),
        .dbg_x28(dbg_x28), .dbg_x29(dbg_x29), .dbg_x30(dbg_x30), .dbg_x31(dbg_x31)
    );

    // ============================================================
    // Gerador de Imediato
    // ============================================================
    wire [31:0] imm;
    imm_gen u_immgen (
        .instruction (instruction),
        .imm         (imm)
    );

    // ============================================================
    // Entradas da ULA
    // ALUSrcA: 00=rs1  01=PC (AUIPC)  10=zero (LUI)
    // ALUSrc:   0=rs2  1=imm
    // ============================================================
    wire [31:0] alu_a = (ALUSrcA == 2'b01) ? pc    :
                        (ALUSrcA == 2'b10) ? 32'd0 : rs1_data;
    wire [31:0] alu_b = ALUSrc ? imm : rs2_data;

    // ============================================================
    // Controle da ULA
    // itype=1 quando opcode=I-type ALU (0010011) — suprime SUB
    // ============================================================
    wire [3:0] alu_ctrl_op;
    wire       itype = (opcode == 7'b0010011);

    alu_control u_aluctrl (
        .ALUOp  (ALUOp),
        .funct3 (funct3),
        .funct7 (funct7),
        .itype  (itype),
        .alu_op (alu_ctrl_op)
    );

    // ============================================================
    // ULA
    // ============================================================
    wire [31:0] alu_result;
    wire        zero;

    alu u_alu (
        .a      (alu_a),
        .b      (alu_b),
        .alu_op (alu_ctrl_op),
        .result (alu_result),
        .zero   (zero)
    );

    // ============================================================
    // Alvo de desvio / salto: PC + imm  (branch e JAL)
    // ============================================================
    wire [31:0] pc_branch = pc + imm;

    // ============================================================
    // Memória de Dados (Harvard — leitura/escrita)
    // ============================================================
    wire [31:0] mem_rdata;

    data_mem u_dmem (
        .clk      (clk),
        .MemWrite (MemWrite),
        .MemRead  (MemRead),
        .funct3   (funct3),
        .addr     (alu_result),
        .wdata    (rs2_data),
        .rdata    (mem_rdata)
    );

    // ============================================================
    // MUX de escrita no banco (ResultSrc)
    // 00 = resultado da ULA
    // 01 = dado lido da memória
    // 10 = PC+4  (JAL / JALR)
    // ============================================================
    assign wr_data = (ResultSrc == 2'b01) ? mem_rdata :
                     (ResultSrc == 2'b10) ? pc_plus4  :
                                            alu_result;

    // ============================================================
    // Lógica do próximo PC
    // Prioridade: JALR > JAL > branch > PC+4
    // ============================================================
    wire branch_taken = Branch & (zero ^ BranchNE);

    assign pc_next = JumpReg      ? {alu_result[31:1], 1'b0} :
                     Jump         ? pc_branch                 :
                     branch_taken ? pc_branch                 :
                                    pc_plus4;

    // ============================================================
    // Atribuições de observação → portas de saída (Virtual Pins)
    // ============================================================
    assign dbg_pc           = pc;
    assign dbg_instr        = instruction;
    assign dbg_alu_result   = alu_result;
    assign dbg_mem_rdata    = mem_rdata;
    assign dbg_wr_data      = wr_data;
    assign dbg_rs1_data     = rs1_data;
    assign dbg_rs2_data     = rs2_data;
    assign dbg_imm          = imm;
    assign dbg_RegWrite     = RegWrite;
    assign dbg_MemWrite     = MemWrite;
    assign dbg_MemRead      = MemRead;
    assign dbg_Branch       = Branch;
    assign dbg_Jump         = Jump;
    assign dbg_JumpReg      = JumpReg;
    assign dbg_ALUOp        = ALUOp;
    assign dbg_ResultSrc    = ResultSrc;
    assign dbg_alu_ctrl_op  = alu_ctrl_op;
    assign dbg_zero         = zero;
    assign dbg_branch_taken = branch_taken;
    assign dbg_mem_wdata    = rs2_data;
    assign dbg_mem_addr     = alu_result;

endmodule