___
# Objetivos
+ Tornar-se familiarizado com o Assembly e as metodologias de aplicação eficientes e otimizadas.
+ Tornar-se crítico à respeito do desempenho real provido pelo sistema operacional.
# Metodologia
+ Desenvolvimento de uma aplicação em python que simulará um RARS.
# Entregáveis
+ Código em Python (arquivo único .py) para a submissão na plataforma [Turnitin] e que atende aos seguintes requisitos:
	+ **Requisito 1**: <font color="#4f81bd">Entrada</font> (arquivo texto ASCII, com extensão .asm) de um código em Assembly RISC-V32I que deverá gerar um código objeto montado em Hexadecimal (arquivo de texto ASCII, com extensão .mif[^3]).
		+ <font color="#4f81bd">Sobre o arquivo de entrada</font>: Uma lista pré-definida de instruções as quais devem estar nas áreas ou .text ou .data. Juntamente com o <font color="#ff0000">"endereçamento para as respectivas áreas, de acordo com o mapa de memória utilizado no ambiente RARS"</font>[^1]. A interface deve ser feita para os arquivos de entrada e a saída, <font color="#ff0000">"utilizando todos os recursos disponíveis no ambiente RARS"</font>[^2].
		+ "A aplicação deve ter como argumento de entrada, o leque de registradores inteiros da CPU, as máscaras atribuídas aos registradores, permitir a entrada no campo imediato de números inteiros, não-sinalizados e sinalizados, valores em hexadecimal (imediatos começando com valores 0xXXXXXXXX de 32 bits de comprimento)."
		+ <font color="#4f81bd">Saída</font>: Um (Dois ?) arquivo (ASCII, com extensão .mif) com o mesmo nome do arquivo de entrada. Um arquivo para cada área .data e .text.
	+ **Requisito 2**: As instruções à serem compiladas e montadas pela aplicação:
		+ lw; add/sub/and/or/xor; addi; sw; jal; jalr; beq/bne; slt; slti; lui; auipc; sll/srl; addi/andi/ori/xori; lhu.
	+ **Requisito 3**: Relatório
# Observações
+ <font color="#ff0000">"O modo de endereçamento, incluindo a informação do cabeçalho</font>[^4], sendo responsabilidade dos desenvolvedores o tratamento dos endereços gerados, incluindo todos os ajustes necessários. Todas as instruções devem ser tratadas, incluindo as possíveis falhas, como `opcode` desconhecido e instrução inexistente".
# Itens de Pesquisa
+ Arquivo .mif (Memory Inicialization File)
+ Áreas de endereçamento de acordo com o mapa de memória do RARS
+ Quais são os recursos disponíveis na entrada e saída do RARS ?

[^1]: O que é isso ? Colocar um link aqui quando fizer a pesquisa.

[^2]: O que isso quer dizer ? Tudo do RARS deve estar na aplicação ou só podemos ter na aplicação o que tem no RARS ? Colocar a resposta aqui quando souber.

[^3]: Sobre a estrutura dos arquivos .mif, pesquisar em: http://wiki.icmc.usp.br/images/f/f1/SSC-118_2016_2_Onchip_Tutorial.pdf

[^4]: O que é isso ?
