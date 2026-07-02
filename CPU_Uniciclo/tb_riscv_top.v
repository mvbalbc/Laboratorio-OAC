`timescale 1ns/1ps

module tb_riscv_top;

    // Sinais de controle
    reg clk;
    reg rst;

    // Instanciando o seu processador (Device Under Test)
    riscv_top DUT (
        .clk(clk),
        .rst(rst)
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