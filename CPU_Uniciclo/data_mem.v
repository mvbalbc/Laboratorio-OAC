// ============================================================
//  data_mem.v — Memória de Dados (RAM, 1024 × 32 bits)
//
//  Arquitetura Harvard: leitura combinacional, escrita síncrona.
//  Base RARS: DATA_BASE = 0x10010000
//
//  Instruções suportadas (via funct3):
//    lw  (funct3=010) — carrega 32 bits
//    lhu (funct3=101) — carrega 16 bits sem sinal
//    sw  (funct3=010) — armazena 32 bits
//
//  Para lhu: addr[1] seleciona o halfword dentro da palavra:
//    addr[1]=0 → bits [15:0]   addr[1]=1 → bits [31:16]
//
//  PREPARAÇÃO:
//    python3 mif2hex.py UnicicloData.mif UnicicloData.hex
// ============================================================
`timescale 1ns / 1ps

module data_mem (
    input  wire        clk,
    input  wire        MemWrite,
    input  wire        MemRead,
    input  wire [2:0]  funct3,
    input  wire [31:0] addr,
    input  wire [31:0] wdata,
    output reg  [31:0] rdata
);

    localparam DATA_BASE = 32'h1001_0000;
    localparam DEPTH     = 1024;

    reg [31:0] mem [0:DEPTH-1];

    integer k;
    initial begin
        for (k = 0; k < DEPTH; k = k + 1)
            mem[k] = 32'd0;
        $readmemh("UnicicloData.hex", mem);
    end

    wire [9:0] word_addr = (addr - DATA_BASE) >> 2;

    // ── Leitura combinacional ──────────────────────────────
    always @(*) begin
        rdata = 32'd0;
        if (MemRead) begin
            case (funct3)
                3'b010: // lw — palavra inteira
                    rdata = mem[word_addr];

                3'b101: // lhu — halfword sem sinal
                    rdata = addr[1]
                            ? {16'd0, mem[word_addr][31:16]}
                            : {16'd0, mem[word_addr][15:0]};

                default:
                    rdata = mem[word_addr];
            endcase
        end
    end

    // ── Escrita síncrona ───────────────────────────────────
    always @(posedge clk) begin
        if (MemWrite) begin
            case (funct3)
                3'b010: mem[word_addr] <= wdata; // sw
                // sh / sb podem ser adicionados aqui se necessário
                default: ; // ignora
            endcase
        end
    end

endmodule
