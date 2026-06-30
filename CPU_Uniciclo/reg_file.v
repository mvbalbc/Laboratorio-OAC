// ============================================================
//  reg_file.v — Banco de Registradores 32×32 bits
//
//  • x0 permanece sempre zero (escrita ignorada, leitura = 0)
//  • Escrita síncrona na borda de subida do clock
//  • Leitura combinacional (assíncrona)
//  • Portas dbg_x0..dbg_x31 expõem todos os registradores
//    para o Waveform Editor
// ============================================================
`timescale 1ns / 1ps

module reg_file (
    input  wire        clk,
    input  wire        RegWrite,
    input  wire [4:0]  rs1,
    input  wire [4:0]  rs2,
    input  wire [4:0]  rd,
    input  wire [31:0] wr_data,
    output wire [31:0] rs1_data,
    output wire [31:0] rs2_data,

    // saídas de depuração — todos os 32 registradores
    output wire [31:0] dbg_x0,  dbg_x1,  dbg_x2,  dbg_x3,
                       dbg_x4,  dbg_x5,  dbg_x6,  dbg_x7,
                       dbg_x8,  dbg_x9,  dbg_x10, dbg_x11,
                       dbg_x12, dbg_x13, dbg_x14, dbg_x15,
                       dbg_x16, dbg_x17, dbg_x18, dbg_x19,
                       dbg_x20, dbg_x21, dbg_x22, dbg_x23,
                       dbg_x24, dbg_x25, dbg_x26, dbg_x27,
                       dbg_x28, dbg_x29, dbg_x30, dbg_x31
);

    reg [31:0] regs [0:31];

    // Inicializa todos os registradores com zero
    integer i;
    initial begin
        for (i = 0; i < 32; i = i + 1)
            regs[i] = 32'd0;
    end

    // ── Escrita síncrona (x0 imune) ─────────────────────────
    always @(posedge clk) begin
        if (RegWrite && (rd != 5'd0))
            regs[rd] <= wr_data;
    end

    // ── Leitura combinacional ───────────────────────────────
    assign rs1_data = (rs1 == 5'd0) ? 32'd0 : regs[rs1];
    assign rs2_data = (rs2 == 5'd0) ? 32'd0 : regs[rs2];

    // ── Saídas de depuração ────────────────────────────────
    assign dbg_x0  = 32'd0;        // x0 hardwired
    assign dbg_x1  = regs[1];
    assign dbg_x2  = regs[2];
    assign dbg_x3  = regs[3];
    assign dbg_x4  = regs[4];
    assign dbg_x5  = regs[5];
    assign dbg_x6  = regs[6];
    assign dbg_x7  = regs[7];
    assign dbg_x8  = regs[8];
    assign dbg_x9  = regs[9];
    assign dbg_x10 = regs[10];
    assign dbg_x11 = regs[11];
    assign dbg_x12 = regs[12];
    assign dbg_x13 = regs[13];
    assign dbg_x14 = regs[14];
    assign dbg_x15 = regs[15];
    assign dbg_x16 = regs[16];
    assign dbg_x17 = regs[17];
    assign dbg_x18 = regs[18];
    assign dbg_x19 = regs[19];
    assign dbg_x20 = regs[20];
    assign dbg_x21 = regs[21];
    assign dbg_x22 = regs[22];
    assign dbg_x23 = regs[23];
    assign dbg_x24 = regs[24];
    assign dbg_x25 = regs[25];
    assign dbg_x26 = regs[26];
    assign dbg_x27 = regs[27];
    assign dbg_x28 = regs[28];
    assign dbg_x29 = regs[29];
    assign dbg_x30 = regs[30];
    assign dbg_x31 = regs[31];

endmodule
