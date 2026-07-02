`timescale 1ns/1ps

module tb_riscv_top;

    // Sinais de controle
    reg clk;
    reg rst;

    // Sinais de observação
    wire [31:0] dbg_pc, dbg_instr, dbg_alu_result, dbg_mem_rdata;
    wire [31:0] dbg_mem_wdata, dbg_mem_addr, dbg_wr_data;
    wire [31:0] dbg_rs1_data, dbg_rs2_data, dbg_imm;
    wire        dbg_RegWrite, dbg_MemWrite, dbg_MemRead;
    wire        dbg_Branch, dbg_Jump, dbg_JumpReg;
    wire [1:0]  dbg_ALUOp, dbg_ResultSrc;
    wire [3:0]  dbg_alu_ctrl_op;
    wire        dbg_zero, dbg_branch_taken;
    wire [31:0] dbg_x0,  dbg_x1,  dbg_x2,  dbg_x3,
                dbg_x4,  dbg_x5,  dbg_x6,  dbg_x7,
                dbg_x8,  dbg_x9,  dbg_x10, dbg_x11,
                dbg_x12, dbg_x13, dbg_x14, dbg_x15,
                dbg_x16, dbg_x17, dbg_x18, dbg_x19,
                dbg_x20, dbg_x21, dbg_x22, dbg_x23,
                dbg_x24, dbg_x25, dbg_x26, dbg_x27,
                dbg_x28, dbg_x29, dbg_x30, dbg_x31;

    // Instanciando o processador (Device Under Test)
    riscv_top DUT (
        .clk(clk), .rst(rst),
        .dbg_pc(dbg_pc), .dbg_instr(dbg_instr),
        .dbg_alu_result(dbg_alu_result), .dbg_mem_rdata(dbg_mem_rdata),
        .dbg_mem_wdata(dbg_mem_wdata), .dbg_mem_addr(dbg_mem_addr),
        .dbg_wr_data(dbg_wr_data),
        .dbg_rs1_data(dbg_rs1_data), .dbg_rs2_data(dbg_rs2_data),
        .dbg_imm(dbg_imm),
        .dbg_RegWrite(dbg_RegWrite), .dbg_MemWrite(dbg_MemWrite),
        .dbg_MemRead(dbg_MemRead), .dbg_Branch(dbg_Branch),
        .dbg_Jump(dbg_Jump), .dbg_JumpReg(dbg_JumpReg),
        .dbg_ALUOp(dbg_ALUOp), .dbg_ResultSrc(dbg_ResultSrc),
        .dbg_alu_ctrl_op(dbg_alu_ctrl_op),
        .dbg_zero(dbg_zero), .dbg_branch_taken(dbg_branch_taken),
        .dbg_x0(dbg_x0),   .dbg_x1(dbg_x1),   .dbg_x2(dbg_x2),   .dbg_x3(dbg_x3),
        .dbg_x4(dbg_x4),   .dbg_x5(dbg_x5),   .dbg_x6(dbg_x6),   .dbg_x7(dbg_x7),
        .dbg_x8(dbg_x8),   .dbg_x9(dbg_x9),   .dbg_x10(dbg_x10), .dbg_x11(dbg_x11),
        .dbg_x12(dbg_x12), .dbg_x13(dbg_x13), .dbg_x14(dbg_x14), .dbg_x15(dbg_x15),
        .dbg_x16(dbg_x16), .dbg_x17(dbg_x17), .dbg_x18(dbg_x18), .dbg_x19(dbg_x19),
        .dbg_x20(dbg_x20), .dbg_x21(dbg_x21), .dbg_x22(dbg_x22), .dbg_x23(dbg_x23),
        .dbg_x24(dbg_x24), .dbg_x25(dbg_x25), .dbg_x26(dbg_x26), .dbg_x27(dbg_x27),
        .dbg_x28(dbg_x28), .dbg_x29(dbg_x29), .dbg_x30(dbg_x30), .dbg_x31(dbg_x31)
    );

    // Gerador de Clock (Período de 20ns)
    initial begin
        clk = 0;
        forever #10 clk = ~clk; // Inverte a cada 10ns
    end

    // Gerador de Reset e Tempo Máximo
    initial begin
        // Força Reset no início
        rst = 1;
        
        // Espera 10ns e desliga o Reset
        #10 rst = 0;

        // Deixa a CPU rodar por 2 microssegundos (2000ns)
        #2000;
        
        // Finaliza a simulação
        $stop;
    end

endmodule