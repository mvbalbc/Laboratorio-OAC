# RISC-V32I Uniciclo — OAC UnB 1o/2026

## Arquivos do projeto

| Arquivo         | Função                                          |
|-----------------|-------------------------------------------------|
| riscv_top.v     | Top-level: datapath completo + saídas de debug  |
| control.v       | Unidade de controle principal                   |
| alu_control.v   | Controle da ULA (decodifica funct3/funct7)      |
| alu.v           | ULA 32 bits (ADD/SUB/AND/OR/XOR/SLT/SLL/SRL)   |
| reg_file.v      | Banco de registradores 32×32, x0 hardwired      |
| imm_gen.v       | Gerador de imediato (I/S/B/U/J)                 |
| inst_mem.v      | Memória de instruções ROM 1024×32               |
| data_mem.v      | Memória de dados RAM 1024×32 (lw/lhu/sw)        |
| mif2hex.py      | Conversor MIF → HEX para $readmemh              |

## Instruções suportadas

R-type : add, sub, and, or, xor, slt, sll, srl  
I-type : addi, andi, ori, xori, slti, slli, srli  
Load   : lw, lhu  
Store  : sw  
Branch : beq, bne  
Jump   : jal, jalr  
U-type : lui, auipc  

## Passo a passo — Quartus II



### 2. Criar o projeto Quartus II

- File → New Project Wizard
- Top-level entity: `riscv_top`
- Adicionar todos os arquivos `.v` ao projeto
- Device: Cyclone II (ou o disponível no lab)

### 3. Compilar

- Processing → Start Compilation  
- Corrigir warnings de latch se aparecerem (todos os `always @(*)` têm `default`)

### 4. Simulação funcional (Waveform Editor)

- File → New → Vector Waveform File (.vwf)
- Edit → Insert Node or Bus → Node Finder  
- Adicionar:
  - `clk`, `rst`
  - `dbg_pc`, `dbg_instr`, `dbg_alu_result`
  - `dbg_rs1_data`, `dbg_rs2_data`, `dbg_wr_data`, `dbg_imm`
  - Sinais de controle: `dbg_RegWrite`, `dbg_MemWrite`, `dbg_Branch`, etc.
  - Registradores: `dbg_x0` … `dbg_x31`
- Configurar clock: período recomendado **50 ns** para funcional
- Simulation → Run Functional Simulation

### 5. Simulação de timing (Requisito 4)

- Assignments → Settings → Simulator Settings → Timing
- Simulation → Run Timing Simulation
- Observar os atrasos de propagação em cada sinal
- O período mínimo de clock é determinado pelo caminho crítico:
  `PC → Inst Mem → Control/ImmGen → RegFile → ALU → Data Mem → RegFile`

### 6. Apresentação

No dia da apresentação o professor fornecerá novos arquivos `.mif`.  
Execute o conversor (`mif2hex.py`) e recompile.  
Todos os 32 registradores devem estar visíveis no waveform.

## Mapa de endereços

| Segmento    | Base         |
|-------------|--------------|
| .text (ROM) | 0x00400000   |
| .data (RAM) | 0x10010000   |

Cada memória tem profundidade de **1024 palavras (4 KB)**.  
Para programas maiores, aumente `DEPTH` em `inst_mem.v` / `data_mem.v`
e ajuste a largura de `word_addr`.
