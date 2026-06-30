##################### BIBLIOTECAS ##########################

from pathlib import Path
import re
import os
import sys

#################### TABELAS DE REGISTRADORES ##############

REG_NAMES = {
    'zero': 0, 'x0': 0,
    'ra': 1,   'x1': 1,
    'sp': 2,   'x2': 2,
    'gp': 3,   'x3': 3,
    'tp': 4,   'x4': 4,
    't0': 5,   'x5': 5,
    't1': 6,   'x6': 6,
    't2': 7,   'x7': 7,
    's0': 8,   'fp': 8,  'x8': 8,
    's1': 9,   'x9': 9,
    'a0': 10,  'x10': 10,
    'a1': 11,  'x11': 11,
    'a2': 12,  'x12': 12,
    'a3': 13,  'x13': 13,
    'a4': 14,  'x14': 14,
    'a5': 15,  'x15': 15,
    'a6': 16,  'x16': 16,
    'a7': 17,  'x17': 17,
    's2': 18,  'x18': 18,
    's3': 19,  'x19': 19,
    's4': 20,  'x20': 20,
    's5': 21,  'x21': 21,
    's6': 22,  'x22': 22,
    's7': 23,  'x23': 23,
    's8': 24,  'x24': 24,
    's9': 25,  'x25': 25,
    's10': 26, 'x26': 26,
    's11': 27, 'x27': 27,
    't3': 28,  'x28': 28,
    't4': 29,  'x29': 29,
    't5': 30,  'x30': 30,
    't6': 31,  'x31': 31,
}

#################### MAPA DE MEMORIA DO RARS ###############

"""
endereços base do RARS para as duas áreas que a gente precisa. A .text começa em 0x00400000 e a .data em 0x10010000
"""

TEXT_BASE = 0x00400000
DATA_BASE = 0x10010000

#################### TABELA DE INSTRUCOES ##################

"""
para cada minemonico eu guardo (formato, opcode, funct3, funct7). Quando o campo nao existe coloco none.
"""
"""
os formatos IS, IM e IJ sao variacoes do tipo I
"""

TABELA_INSTRUCOES = {
    'add':   ('R',  0x33, 0x0, 0x00),
    'sub':   ('R',  0x33, 0x0, 0x20),
    'and':   ('R',  0x33, 0x7, 0x00),
    'or':    ('R',  0x33, 0x6, 0x00),
    'xor':   ('R',  0x33, 0x4, 0x00),
    'sll':   ('R',  0x33, 0x1, 0x00),
    'srl':   ('R',  0x33, 0x5, 0x00),
    'slt':   ('R',  0x33, 0x2, 0x00),
    'addi':  ('I',  0x13, 0x0, None),
    'andi':  ('I',  0x13, 0x7, None),
    'ori':   ('I',  0x13, 0x6, None),
    'xori':  ('I',  0x13, 0x4, None),
    'slti':  ('I',  0x13, 0x2, None),
    'slli':  ('IS', 0x13, 0x1, 0x00),
    'srli':  ('IS', 0x13, 0x5, 0x00),
    'srai':  ('IS', 0x13, 0x5, 0x20),
    'lw':    ('IM', 0x03, 0x2, None),
    'lhu':   ('IM', 0x03, 0x5, None),
    'jalr':  ('IJ', 0x67, 0x0, None),
    'sw':    ('S',  0x23, 0x2, None),
    'beq':   ('B',  0x63, 0x0, None),
    'bne':   ('B',  0x63, 0x1, None),
    'lui':   ('U',  0x37, None, None),
    'auipc': ('U',  0x17, None, None),
    'jal':   ('J',  0x6F, None, None),
}

#################### ENTRADA DO ARQUIVO ####################

def entrada_arquivo(caminho):
    """ verifica se o arquivo existe e se tem a extensao .asm """
    p = Path(caminho)
    if p.suffix.lower() != '.asm':
        print(f"arquivo precisa ter extensao .asm (recebi '{p.name}')")
        return None
    if not p.exists():
        print(f"o arquivo '{caminho}' nao foi encontrado")
        return None
    return p

##################### LEITURA DE ARQUIVO ###################

def ler_arquivo(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as arq:
        conteudo = arq.readlines()
    return conteudo

#################### TRATAMENTO DAS LINHAS #################

def tratar_ws(linhas_arquivo):
    linhas_tratadas = []

    for linha in linhas_arquivo:
        saida = []
        dentro_de_aspas = False
        for c in linha:
            if c == '"':
                dentro_de_aspas = not dentro_de_aspas
            if c == '#' and not dentro_de_aspas:
                break
            saida.append(c)
        linha_limpa = ''.join(saida).rstrip()
        linha_limpa = linha_limpa.strip()

        if linha_limpa:
            linhas_tratadas.append(linha_limpa)
    return linhas_tratadas

##################### PARTICIONA AS SECOES #################

"""
separa o .data do .text
"""

def particionar_secoes(linhas):
    linhas_text = []
    linhas_data = []
    secao_atual = None

    for numero, linha in enumerate(linhas, start=1):
        baixa = linha.lower()

        if baixa.startswith('.data'):
            secao_atual = linhas_data
            resto = linha[5:].strip()
            if resto:
                secao_atual.append((numero, resto))
            continue

        if baixa.startswith('.text'):
            secao_atual = linhas_text
            resto = linha[5:].strip()
            if resto:
                secao_atual.append((numero, resto))
            continue

        if secao_atual is not None:
            secao_atual.append((numero, linha))
    return linhas_text, linhas_data

###################### TIPO-R ##############################

class TipoR:
    def __init__(self, opcode, rd, funct3, rs1, rs2, funct7):
        self.opcode = f"{opcode & 0x7F:07b}"
        self.rd     = f"{rd     & 0x1F:05b}"
        self.funct3 = f"{funct3 & 0x07:03b}"
        self.rs1    = f"{rs1    & 0x1F:05b}"
        self.rs2    = f"{rs2    & 0x1F:05b}"
        self.funct7 = f"{funct7 & 0x7F:07b}"

    def montar(self):
        return self.funct7 + self.rs2 + self.rs1 + self.funct3 + self.rd + self.opcode

"""entre regists"""

###################### TIPO-I ##############################

class TipoI:
    def __init__(self, opcode, rd, funct3, rs1, imm):
        self.opcode = f"{opcode & 0x7F:07b}"
        self.rd     = f"{rd     & 0x1F:05b}"
        self.funct3 = f"{funct3 & 0x07:03b}"
        self.rs1    = f"{rs1    & 0x1F:05b}"
        self.imm    = f"{imm    & 0xFFF:012b}"

    def montar(self):
        return self.imm + self.rs1 + self.funct3 + self.rd + self.opcode

"""pequeno de 12 bits"""

###################### TIPO-S ##############################

class TipoS:
    def __init__(self, opcode, funct3, rs1, rs2, imm):
        self.opcode = f"{opcode & 0x7F:07b}"
        self.funct3 = f"{funct3 & 0x07:03b}"
        self.rs1    = f"{rs1    & 0x1F:05b}"
        self.rs2    = f"{rs2    & 0x1F:05b}"
        imm_bin = f"{imm & 0xFFF:012b}"
        self.imm11_5 = imm_bin[0:7]
        self.imm4_0  = imm_bin[7:12]

    def montar(self):
        return self.imm11_5 + self.rs2 + self.rs1 + self.funct3 + self.imm4_0 + self.opcode

"""salva dados na memoria"""

###################### TIPO-B ##############################

class TipoB:
    def __init__(self, opcode, funct3, rs1, rs2, imm):
        self.opcode = f"{opcode & 0x7F:07b}"
        self.funct3 = f"{funct3 & 0x07:03b}"
        self.rs1    = f"{rs1    & 0x1F:05b}"
        self.rs2    = f"{rs2    & 0x1F:05b}"
        imm_bin = f"{imm & 0x1FFF:013b}"
        self.imm12   = imm_bin[0]
        self.imm11   = imm_bin[1]
        self.imm10_5 = imm_bin[2:8]
        self.imm4_1  = imm_bin[8:12]

    def montar(self):
        return (self.imm12 + self.imm10_5 + self.rs2 + self.rs1 +
                self.funct3 + self.imm4_1 + self.imm11 + self.opcode)

"""tipo um if, se der bom da um salto curto"""

###################### TIPO-U ##############################

class TipoU:
    def __init__(self, opcode, rd, imm):
        self.opcode = f"{opcode & 0x7F:07b}"
        self.rd     = f"{rd     & 0x1F:05b}"
        self.imm    = f"{imm    & 0xFFFFF:020b}"

    def montar(self):
        return self.imm + self.rd + self.opcode

"""carrega n grande de bits no registrador"""

###################### TIPO-J ##############################

class TipoJ:
    def __init__(self, opcode, rd, imm):
        self.opcode = f"{opcode & 0x7F:07b}"
        self.rd     = f"{rd     & 0x1F:05b}"
        imm_bin = f"{imm & 0x1FFFFF:021b}"
        self.imm20    = imm_bin[0]
        self.imm19_12 = imm_bin[1:9]
        self.imm11    = imm_bin[9]
        self.imm10_1  = imm_bin[10:20]

    def montar(self):
        return (self.imm20 + self.imm10_1 + self.imm11 +
                self.imm19_12 + self.rd + self.opcode)

"""salto longo"""

################### PARSING DE OPERANDOS ###################

def pegar_registrador(token):
    """ aceita 'zero', 'ra', 't0', 'x5', e tals, Retorna o numero de 0 a 31"""
    t = token.strip().lower()
    if t not in REG_NAMES:
        raise ValueError(f"registrador invalido: '{token}'")
    return REG_NAMES[t]


def pegar_imediato(token, dicionario_labels=None):
    """
    aceita decimal, hexadecimal e negativos
    """
    t = token.strip()

    m = re.match(r'(?i)%hi\(\s*(\w+)\s*\)', t)
    if m:
        rotulo = m.group(1)
        if not dicionario_labels or rotulo not in dicionario_labels:
            raise ValueError(f"label não definida em %hi: '{rotulo}'")
        endereco = dicionario_labels[rotulo]
        return ((endereco + 0x800) >> 12) & 0xFFFFF

    m = re.match(r'(?i)%lo\(\s*(\w+)\s*\)', t)
    if m:
        rotulo = m.group(1)
        if not dicionario_labels or rotulo not in dicionario_labels:
            raise ValueError(f"label não definida em %lo: '{rotulo}'")
        endereco = dicionario_labels[rotulo]
        baixo = endereco & 0xFFF
        return baixo - 0x1000 if baixo >= 0x800 else baixo

    try:
        return int(t, 0)
    except ValueError:
        raise ValueError(f"imediato invalido: '{token}'")


def pegar_operando_memoria(token):
    """ quebra um operando do tipo 'imediato(registrador)', tipo '4(t1)' """
    m = re.match(r'^(.*?)\(\s*(\w+)\s*\)\s*$', token.strip())
    if not m:
        raise ValueError(f"operando de memoria mal formado: '{token}'")
    return m.group(1).strip(), m.group(2).strip()


def quebrar_operandos(resto_da_linha):
    """ recebe 'rd, rs1, imm' e devolve ['rd', 'rs1', 'imm'] """
    return [x.strip() for x in resto_da_linha.split(',') if x.strip()]


def pegar_alvo_branch(token, pc_atual, dicionario_labels):
    """
    para branches e jumps, o operando pode ser um label ou um num msm
    """
    if dicionario_labels and token in dicionario_labels:
        return dicionario_labels[token] - pc_atual
    return pegar_imediato(token, dicionario_labels)

################# CODIFICAR UMA INSTRUCAO ##################

def codificar_instrucao(mnemonico, pedacos, pc=0, dicionario_labels=None):
    """
    funcao principal do montas. Recebe o mnemonico e a lista de operandos e devlve a string de 32 bits
    """
    mnemonico = mnemonico.lower()
    if mnemonico not in TABELA_INSTRUCOES:
        raise ValueError(f"opcode desconhecido: '{mnemonico}'")

    formato, opcode, funct3, funct7 = TABELA_INSTRUCOES[mnemonico]

    if formato == 'R':
        if len(pedacos) != 3:
            raise ValueError(f"{mnemonico}: esperados 3 operandos")
        rd  = pegar_registrador(pedacos[0])
        rs1 = pegar_registrador(pedacos[1])
        rs2 = pegar_registrador(pedacos[2])
        return TipoR(opcode, rd, funct3, rs1, rs2, funct7).montar()

    if formato == 'I':
        if len(pedacos) != 3:
            raise ValueError(f"{mnemonico}: esperados 3 operandos")
        rd  = pegar_registrador(pedacos[0])
        rs1 = pegar_registrador(pedacos[1])
        imm = pegar_imediato(pedacos[2], dicionario_labels)
        return TipoI(opcode, rd, funct3, rs1, imm).montar()

    if formato == 'IS':
        if len(pedacos) != 3:
            raise ValueError(f"{mnemonico}: esperados 3 operandos")
        rd    = pegar_registrador(pedacos[0])
        rs1   = pegar_registrador(pedacos[1])
        shamt = pegar_imediato(pedacos[2], dicionario_labels) & 0x1F
        imm   = (funct7 << 5) | shamt
        return TipoI(opcode, rd, funct3, rs1, imm).montar()

    if formato == 'IM':
        if len(pedacos) != 2:
            raise ValueError(f"{mnemonico}: esperado formato rd, imm(rs1)")
        rd = pegar_registrador(pedacos[0])
        parte_imm, parte_rs1 = pegar_operando_memoria(pedacos[1])
        rs1 = pegar_registrador(parte_rs1)
        imm = pegar_imediato(parte_imm, dicionario_labels)
        return TipoI(opcode, rd, funct3, rs1, imm).montar()

    if formato == 'IJ':
        rd = pegar_registrador(pedacos[0])
        if len(pedacos) == 2:
            parte_imm, parte_rs1 = pegar_operando_memoria(pedacos[1])
            rs1 = pegar_registrador(parte_rs1)
            imm = pegar_imediato(parte_imm, dicionario_labels)
        elif len(pedacos) == 3:
            rs1 = pegar_registrador(pedacos[1])
            imm = pegar_imediato(pedacos[2], dicionario_labels)
        else:
            raise ValueError("jalr: número de operandos inválido")
        return TipoI(opcode, rd, funct3, rs1, imm).montar()

    if formato == 'S':
        if len(pedacos) != 2:
            raise ValueError(f"{mnemonico}: esperado formato rs2, imm(rs1)")
        rs2 = pegar_registrador(pedacos[0])
        parte_imm, parte_rs1 = pegar_operando_memoria(pedacos[1])
        rs1 = pegar_registrador(parte_rs1)
        imm = pegar_imediato(parte_imm, dicionario_labels)
        return TipoS(opcode, funct3, rs1, rs2, imm).montar()

    if formato == 'B':
        if len(pedacos) != 3:
            raise ValueError(f"{mnemonico}: esperados 3 operandos")
        rs1 = pegar_registrador(pedacos[0])
        rs2 = pegar_registrador(pedacos[1])
        imm = pegar_alvo_branch(pedacos[2], pc, dicionario_labels)
        if imm % 2 != 0:
            raise ValueError(f"{mnemonico}: offset de branch precisa ser par")
        return TipoB(opcode, funct3, rs1, rs2, imm).montar()

    if formato == 'U':
        if len(pedacos) != 2:
            raise ValueError(f"{mnemonico}: esperados 2 operandos")
        rd  = pegar_registrador(pedacos[0])
        imm = pegar_imediato(pedacos[1], dicionario_labels)
        return TipoU(opcode, rd, imm & 0xFFFFF).montar()

    if formato == 'J':
        if len(pedacos) == 1:
            rd  = REG_NAMES['ra']
            imm = pegar_alvo_branch(pedacos[0], pc, dicionario_labels)
        elif len(pedacos) == 2:
            rd  = pegar_registrador(pedacos[0])
            imm = pegar_alvo_branch(pedacos[1], pc, dicionario_labels)
        else:
            raise ValueError("jal: nume de operando invlido")
        if imm % 2 != 0:
            raise ValueError(f"{mnemonico}: offset de jal tem q ser par")
        return TipoJ(opcode, rd, imm).montar()
    raise ValueError(f"formato '{formato}' ainda nao tem kk")

################# MONTAGEM DA SECAO .DATA ##################
"""
vai vendo as .word, .half, .string e tals e vai colocando os bytes em um pilha em um vetor
"""
"""
quando vem o rotulo (nome), gaurdo o adress atual na tabelinha o usar o .text dps
"""

ESCAPES = {'n': '\n', 't': '\t', 'r': '\r', '0': '\0',
           '\\': '\\', '"': '"', "'": "'"}


def decodificar_string(literal):
    """ trata escapes tipo \\n, \\t, \\0, e depois converte pra bytes UTF-8 """
    saida = []
    i = 0
    while i < len(literal):
        c = literal[i]
        if c == '\\' and i + 1 < len(literal):
            saida.append(ESCAPES.get(literal[i + 1], literal[i + 1]))
            i += 2
        else:
            saida.append(c)
            i += 1
    return ''.join(saida).encode('utf-8')


def montar_data(linhas_data):
    lista_bytes = bytearray()
    dicionario_labels = {}

    def alinhar(n):
        while len(lista_bytes) % n != 0:
            lista_bytes.append(0)

    for numero, linha in linhas_data:
        while True:
            m = re.match(r'^(\w+)\s*:\s*(.*)$', linha)
            if not m:
                break
            dicionario_labels[m.group(1)] = DATA_BASE + len(lista_bytes)
            linha = m.group(2).strip()
            if not linha:
                break
        if not linha:
            continue
        partes = linha.split(None, 1)
        diretiva = partes[0].lower()
        argumentos = partes[1] if len(partes) > 1 else ''

        try:
            if diretiva == '.word':
                alinhar(4)
                for v in argumentos.split(','):
                    numero_int = int(v.strip(), 0)
                    lista_bytes.extend((numero_int & 0xFFFFFFFF).to_bytes(4, 'little'))

            elif diretiva == '.half':
                alinhar(2)
                for v in argumentos.split(','):
                    numero_int = int(v.strip(), 0)
                    lista_bytes.extend((numero_int & 0xFFFF).to_bytes(2, 'little'))

            elif diretiva == '.byte':
                for v in argumentos.split(','):
                    lista_bytes.append(int(v.strip(), 0) & 0xFF)

            elif diretiva in ('.string', '.asciz', '.asciiz'):
                m = re.match(r'^"(.*)"\s*$', argumentos)
                if not m:
                    raise ValueError("string mal formada")
                lista_bytes.extend(decodificar_string(m.group(1)))
                lista_bytes.append(0)

            elif diretiva == '.ascii':
                m = re.match(r'^"(.*)"\s*$', argumentos)
                if not m:
                    raise ValueError("string mal formada")
                lista_bytes.extend(decodificar_string(m.group(1)))

            elif diretiva == '.space' or diretiva == '.zero':
                lista_bytes.extend(b'\x00' * int(argumentos.strip(), 0))

            elif diretiva == '.align':
                alinhar(1 << int(argumentos.strip(), 0))

            else:
                raise ValueError(f"diretiva desconhecida em .data: '{diretiva}'")

        except ValueError as e:
            raise ValueError(f"linha {numero}: {e}") from None

    while len(lista_bytes) % 4 != 0:
        lista_bytes.append(0)
    palavras = []
    for i in range(0, len(lista_bytes), 4):
        palavras.append(int.from_bytes(lista_bytes[i:i + 4], 'little'))
    return palavras, dicionario_labels

################# MONTAGEM DA SECAO .TEXT ##################
"""
faz duaas passagens no .text, pra pegar o endreco de cada label e dps codifcar em em binario
"""

def primeira_passagem(linhas_text):
    dicionario_labels = {}
    pc = TEXT_BASE
    for numero, linha in linhas_text:
        while True:
            m = re.match(r'^(\w+)\s*:\s*(.*)$', linha)
            if not m:
                break
            dicionario_labels[m.group(1)] = pc
            linha = m.group(2).strip()
            if not linha:
                break
        if linha:
            pc += 4
    return dicionario_labels


def segunda_passagem(linhas_text, dicionario_labels):
    palavras = []
    pc = TEXT_BASE
    for numero, linha_original in linhas_text:
        linha = linha_original
        while True:
            m = re.match(r'^(\w+)\s*:\s*(.*)$', linha)
            if not m:
                break
            linha = m.group(2).strip()
            if not linha:
                break
        if not linha:
            continue

        try:
            partes = linha.split(None, 1)
            mnemonico = partes[0]
            if len(partes) > 1:
                pedacos = quebrar_operandos(partes[1])
            else:
                pedacos = []
            bits = codificar_instrucao(mnemonico, pedacos,
                                       pc=pc, dicionario_labels=dicionario_labels)
            
            comentario_rars = f"% {numero}: {linha_original} %"
            palavras.append((int(bits, 2), comentario_rars))
            
        except ValueError as e:
            raise ValueError(f"linha {numero}: {e}") from None
        pc += 4
    return palavras

################# GERACAO DO ARQUIVO MIF ###################

def gerar_arquivo_mif(caminho_saida, palavras, depth, eh_data=False):
    """
    escreve o file no padrao do mif, imprime os comentarios se houver.
    Se for o .data, ele trava em 1024 pra ficar gigante igual o gabarito.
    Se for o .text, so imprime as linhas certas.
    """
    with open(caminho_saida, 'w', encoding='ascii') as f:
        f.write(f"DEPTH = {depth};\n")
        f.write("WIDTH = 32;\n")
        f.write("ADDRESS_RADIX = HEX;\n")
        f.write("DATA_RADIX = HEX;\n")
        f.write("CONTENT\n")
        f.write("BEGIN\n")
        
        if eh_data:
            limite = 1024
        else:
            limite = len(palavras) if palavras else 1
            
        for i in range(limite):
            if i < len(palavras):
                item = palavras[i]
                if isinstance(item, tuple):
                    valor, coments = item
                    f.write(f"{i:08x} : {valor:08x};   {coments}\n")
                else:
                    f.write(f"{i:08x} : {item:08x};\n")
            else:
                f.write(f"{i:08x} : {0:08x};\n")
                
        f.write("END;\n")

###################### MAIN ################################

if __name__ == '__main__':
    print("jarvis, ligar o simulador de rars\n")
    
    """
    O verificador chama o assembler passndo o caminho do .asm pela linha de comando, ai pega no sys.argv
    """
    if len(sys.argv) > 1:
        nome_arquivo = sys.argv[1]
    else:
        nome_arquivo = "exemplo-lab1.asm"
    caminho_asm = entrada_arquivo(nome_arquivo)

    if caminho_asm:
        try:
            conteudo_original = ler_arquivo(caminho_asm)
            conteudo_limpo = tratar_ws(conteudo_original)

            linhas_text, linhas_data = particionar_secoes(conteudo_limpo)
            palavras_data, simbolos_data = montar_data(linhas_data)

            simbolos_text = primeira_passagem(linhas_text)
            dicionario_labels = {**simbolos_data, **simbolos_text}
            palavras_text = segunda_passagem(linhas_text, dicionario_labels)

            base = caminho_asm.parent / caminho_asm.stem
            saida_text = base.with_name(base.name + '.text.mif')
            saida_data = base.with_name(base.name + '.data.mif')

            gerar_arquivo_mif(saida_text, palavras_text, depth=16384, eh_data=False)
            gerar_arquivo_mif(saida_data, palavras_data, depth=32768, eh_data=True)

            print(f"aqui estao os arquivos senhor, {saida_text} e {saida_data}")

        except ValueError as erro:
            print(f"erro de montagem: {erro}")
            sys.exit(1)

        except Exception:
            print("alguma coisa de errado nao esta certa, jarvis fez cagada")
            sys.exit(1)

################# IDEIAS SOBRE O CÓDIGO ####################

"""
A memoria RAM pode ser uma tabela hash em que geramos o endereço em hexadecimal como a chave e colocamos o conteudo como valor;

Se quisermos ser rígidos com os caracteres de entrada do arquivo lido podemos mudar o tipo de encoding para 'ascii' assim, qualquer caracter que nao for ascii 
gerará uma exceção.

Estou pegando um arquivo em .asm e lendo ele como se fosse .txt, existe algum erro possível nisso ?

arquivo.flush()
re.sub(r'#.*', '', linha).strip()
re.sub(r'\\s+', ' ', linha_limpa)
"""
