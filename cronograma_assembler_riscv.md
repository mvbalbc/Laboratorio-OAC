# Cronograma — Assembler RISC-V32I
**Disciplina:** Organização e Arquitetura de Computadores – Turma 03
**Entrega:** 14/05/2026 até às 23h

---

## Fase 1 — Pesquisa e fundamentos
`23 abr – 26 abr`

- [ ] Estudar o formato de arquivo `.mif` (Memory Initialization File)
  - [ ] Analisar estrutura: cabeçalho, modos de endereçamento, seções
  - [ ] Referência: http://wiki.icmc.usp.br/images/f/f1/SSC-118_2016_2_Onchip_Tutorial.pdf
- [ ] Mapear a memória do RARS
  - [ ] Levantar endereços base das áreas `.text` e `.data`
  - [ ] Anotar limites e convenções do padrão RISC-V32I
- [ ] Levantar todos os formatos de instrução do Requisito 2
  - [ ] Tabelas de opcode, funct3, funct7 para cada instrução
  - [ ] Cobrir todos os tipos: R, I, S, B, U, J
- [ ] Instalar e explorar o RARS
  - [ ] Montar os arquivos `.asm` de exemplo fornecidos pelo professor
  - [ ] Verificar os recursos de entrada/saída disponíveis
- [ ] Definir a arquitetura geral da aplicação Python
  - [ ] Listar módulos: lexer, parser, tabela de símbolos, encoder, gerador de `.mif`, interface I/O
  - [ ] Distribuir responsabilidades entre os membros do grupo

---

## Fase 2 — Núcleo do montador (core)
`27 abr – 05 mai`

- [ ] Implementar o **lexer / tokenizador**
  - [ ] Reconhecer mnemônicos de instrução
  - [ ] Reconhecer registradores por número (`x0`–`x31`) e por alias ABI (`zero`, `ra`, `sp`…)
  - [ ] Reconhecer imediatos decimais, negativos e hexadecimais (`0xXXXXXXXX`)
  - [ ] Reconhecer labels, diretivas `.text` e `.data`
- [ ] Implementar o **parser de 2 passagens**
  - [ ] 1ª passagem: coletar todas as labels → montar tabela de símbolos com endereços absolutos
  - [ ] 2ª passagem: gerar código objeto usando a tabela de símbolos
- [ ] Codificar as instruções **R-type**
  - [ ] `add`, `sub`, `and`, `or`, `xor`
  - [ ] `slt`, `sll`, `srl`
- [ ] Codificar as instruções **I-type**
  - [ ] `addi`, `andi`, `ori`, `xori`, `slti`
  - [ ] `lw`, `lhu`
  - [ ] `jalr`
- [ ] Codificar as instruções **S-type**
  - [ ] `sw`
- [ ] Codificar as instruções **B-type**
  - [ ] `beq`, `bne`
- [ ] Codificar as instruções **U-type**
  - [ ] `lui`, `auipc`
- [ ] Codificar as instruções **J-type**
  - [ ] `jal`
- [ ] Tratar a seção `.data`
  - [ ] Parsear diretivas de dados (`.word`, `.byte`, `.space`, strings)
  - [ ] Alocar endereços conforme o mapa de memória do RARS
- [ ] Calcular offsets e imediatos corretamente
  - [ ] PC-relative para `beq`, `bne`, `jal`
  - [ ] Endereços absolutos para `lui`, `auipc`
  - [ ] Extensão de sinal para imediatos dos tipos I, S e B
- [ ] Implementar tratamento de erros
  - [ ] Opcode desconhecido
  - [ ] Instrução inexistente
  - [ ] Label não definida
  - [ ] Imediato fora do range permitido
  - [ ] Exibir mensagens claras ao usuário para cada caso

---

## Fase 3 — Gerador .mif e interface I/O
`06 mai – 09 mai`

- [ ] Implementar o **gerador de arquivos `.mif`**
  - [ ] Gerar cabeçalho correto: `WIDTH`, `DEPTH`, `ADDRESS_RADIX`, `DATA_RADIX`
  - [ ] Gerar seção `CONTENT BEGIN … END` com endereços e dados em hex
  - [ ] Produzir um arquivo `.mif` para a área `.text` e outro para a área `.data`
  - [ ] Nomear os arquivos de saída com o mesmo nome base do `.asm` de entrada
- [ ] Implementar a **interface de entrada/saída**
  - [ ] Por terminal via `argparse`: seleção de arquivo `.asm` e caminho de saída
  - [ ] (Opcional) GUI simples com `tkinter`
  - [ ] Exibir erros e warnings de forma clara durante a execução
- [ ] Consolidar tudo em **arquivo único `.py`**
  - [ ] Mover todo o código para um único arquivo (requisito do Turnitin)
  - [ ] Adicionar comentários no topo com as instruções de compilação e execução
- [ ] Verificar compatibilidade com **Linux**
  - [ ] Testar separadores de caminho e encoding ASCII/UTF-8
  - [ ] Garantir que `argparse` funciona corretamente no ambiente de correção

---

## Fase 4 — Testes e validação
`10 mai – 12 mai`

- [ ] Testar com os **3 arquivos de exemplo** fornecidos pelo professor
  - [ ] Comparar bit a bit os `.mif` gerados com os `.mif` esperados
- [ ] Executar **testes de casos-limite**
  - [ ] Imediatos máximos e mínimos de cada tipo de instrução
  - [ ] Label definida no início e no final do arquivo
  - [ ] Registradores referenciados por alias (`zero`, `ra`, `sp`…) e por número (`x0`, `x1`…)
  - [ ] Valores hexadecimais no campo imediato (`0xFFFFFFFF`)
- [ ] Testar o **tratamento de erros**
  - [ ] Opcode inválido no arquivo de entrada
  - [ ] Label duplicada
  - [ ] Imediato fora do range permitido
  - [ ] Seção `.text` ou `.data` ausente
- [ ] Corrigir os bugs encontrados
  - [ ] Priorizar erros que causam saída incorreta
  - [ ] Corrigir mensagens de erro imprecisas

---

## Fase 5 — Relatório e entrega
`13 mai – 14 mai`

- [ ] Redigir o **relatório no template LaTeX** (disponível no Aprender3)
  - [ ] i. Identificação: título, data, disciplina/turma, nomes, matrículas e e-mails
  - [ ] ii. Objetivos: descrição sucinta dos objetivos do laboratório
  - [ ] iii. Introdução: teoria sobre RISC-V32I, formatos de instrução e arquivo `.mif`
  - [ ] iv. Materiais e Métodos: ferramentas usadas, arquitetura do código, procedimento adotado
  - [ ] v. Resultados: saídas geradas, tabelas de instruções codificadas, comparação com os exemplos
  - [ ] vi. Discussão e Conclusões: análise de desempenho, pontos críticos a melhorar
  - [ ] vii. Bibliografia: fontes citadas no formato exigido (autor, título, editora, edição, ano, páginas)
- [ ] Realizar a **avaliação quantitativa de desempenho** (Requisito 3)
  - [ ] Medir tempo de montagem para arquivos `.asm` de diferentes tamanhos
  - [ ] Identificar e documentar gargalos de desempenho
- [ ] **Revisão final**
  - [ ] Verificar que o `.py` contém as diretrizes de execução no cabeçalho
  - [ ] Verificar identificação do grupo no código e no relatório
  - [ ] Aceitar os termos de uso do Turnitin no Aprender3
  - [ ] Gerar o PDF final do relatório
- [ ] **Submissão pelo líder no Aprender3** até às 23h do dia 14/05
  - [ ] Arquivo `.py` único
  - [ ] Relatório em PDF
