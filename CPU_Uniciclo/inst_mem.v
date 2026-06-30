// ============================================================
//  inst_mem.v — Memória de Instruções (ROM, 1024 × 32 bits)
//
//  Arquitetura Harvard: somente leitura, sem clock.
//  Base RARS: TEXT_BASE = 0x00400000
//
//  PREPARAÇÃO DO ARQUIVO DE INICIALIZAÇÃO:
//    1. Converta UnicicloInst.mif → UnicicloInst.hex usando:
//         python3 mif2hex.py UnicicloInst.mif UnicicloInst.hex
//    2. Copie UnicicloInst.hex para a pasta do projeto Quartus.
//
//  ALTERNATIVA (Quartus nativo com MIF):
//    Substitua este módulo por uma instância altsyncram com
//    parâmetro INIT_FILE = "UnicicloInst.mif", operação ROM,
//    WIDTH=32, DEPTH=1024, outdata_reg_a="UNREGISTERED".
// ============================================================
`timescale 1ns / 1ps

module inst_mem (
    input  wire [31:0] addr,
    output wire [31:0] rdata
);

    localparam TEXT_BASE = 32'h0040_0000;
    localparam DEPTH     = 1024; // 4 KB — ajuste se necessário

    reg [31:0] mem [0:DEPTH-1];

    integer j;
    initial begin
        // Preenche com NOP (addi x0, x0, 0)
        for (j = 0; j < DEPTH; j = j + 1)
            mem[j] = 32'h0000_0013;
        // Carrega programa compilado
        $readmemh("UnicicloInst.hex", mem);
    end

    // Leitura combinacional — mapeia PC → índice da ROM
    wire [9:0] word_addr = (addr - TEXT_BASE) >> 2;
    assign rdata = mem[word_addr];

endmodule
