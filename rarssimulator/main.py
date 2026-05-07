##################### BIBLIOTECAS ##########################

from pathlib import Path
import re
import tempfile
import os

#################### ENTRADA DO ARQUIVO ####################

def entrada_arquivo(nome_arquivo):
    arquivos_asm = list(Path('.').glob('*.asm'))
    nome_completo_arquivo = f"{nome_arquivo}" + ".asm"
    if arquivos_asm:
        if Path(nome_completo_arquivo).exists():
            print(f"O arquivo de nome {nome_completo_arquivo} existe.")
            return nome_completo_arquivo
        else:
            print(f"O nome do arquivo não foi encontrado")
            print(arquivos_asm)

    else:
        print(f"Nenhum arquivo .asm foi encontrado.")
        return None

##################### LEITURA DE ARQUIVO #######################

def ler_arquivo(arquivo):
    print("Lendo arquivo")
    with open(arquivo, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.readlines()
    return conteudo

##################### EXECUCAO DO CODIGO #######################
"""
Penso que essa função será como o PC do código em Assembly
"""

def executa_codigo(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            ## Estamos assumindo que só temos os dois campos de códigos ".data" e ".text"
            if linha == ".data":
                for linha in arquivo: ## Veja se continua do mesmo ponto do arquivo
                    if linha == ".text":
                        break

            if linha == ".text":
                for linha in arquivo:
                    if linha == ".data":
                        break
            partes = linha.strip().split()
            instrucao = partes[0]
            try:
                operandos: partes[1:] # Estamos tentando achar as instruções que não tem os operandos
            except:
                print("Instrução sem operandos")
            
        print("chegamos aqui")

#################### TRATAMENTO DO CONTEUDO DO ARQUIVO ########

def tratar_ws(linhas_arquivo):
    """
    Podemos fazer tratamentos das linhas mais sofisticados
    """
    print("Tratando as linhas do arquivo...")
    linhas_tratadas = []
    
    for linha in linhas_arquivo:
        linha_limpa = re.sub(r'#.*', '', linha).strip()
        
        linha_limpa = re.sub(r'\s+', ' ', linha_limpa)

        linha_limpa = linha_limpa.lower()
        
        if linha_limpa:
            linhas_tratadas.append(linha_limpa)
            
    return linhas_tratadas

#################### CRIACAO DO ARQUIVO TEMPORARIO ############

def cria_arquivo_temp(nome_arquivo):
    print("Criando arquivo temporário")
    arquivo_temp = tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8', dir='.')
    return arquivo_temp
     
################### ALTERAR O ARQUIVO TEMPORARIO #############
 
def alterar_arquivo_temp(linhas_codigo, arquivo_temp):
    print("Alterando o arquivo")
    for linha in linhas_codigo:
        arquivo_temp.write(linha + '\n')
    arquivo_temp.flush()
    arquivo_temp.seek(0)
    return arquivo_temp.name # Retornamos o caminho para a próxima função

################# CLASSE RAM ##################################

class RAM:
    def __init__(self):
        self.memoria = {}
    
    def write(self, endereco, valor):
        self.memoria[endereco] = valor

    def read(self, endereco):
        self.memoria.get(endereco, 0)

################# CLASSE TIPO-I ##############################
class TipoI:
    def __init__(self, opcode, rd, funct3, rs1, imm):
        self.rd = f"{rd:05b}"
        self.rs1 = f"{rs1:05b}"
        self.opcode = f"{opcode:07b}"
        self.imm = f"{imm & 0xFFF:012b}"
        self.funct3 = f"{funct3:03b}"
    
    def montar(self):
        return self.rd + self.rs1 + self.opcode + self.imm + self.funct3

"""registrador com n pequeno de bits (12)"""
################## CLASSE TIPO-U #############################    
class TipoU:
    def __init__(self, rd, opcode, imm):
        self.rd = f"{rd:05b}"
        self.opcode = f"{opcode:07b}"
        self.imm = f"{imm & 0xFFFFF:020b}"

    def montar(self):
        return self.rd + self.opcode + self.imm
    
"""carregar n grande de bits no registrador (20)"""
################## CLASSE TIPO-J #############################
class TipoJ:
    def __init__(self, rd, opcode, imm):
        self.rd = f"{rd:05b}"
        self.opcode = f"{opcode:07b}"
        imm_bin = f"{imm & 0x1FFFFF:021b}"
        self.imm10_1 = imm_bin[10:20]
        self.imm19_12 = imm_bin[1:9]
        self.imm11 = imm_bin[9]
        self.imm20 = imm_bin[0]

    def montar(self):
        return self.rd + self.opcode + self.imm10_1 + self.imm19_12 + self.imm11 + self.imm20

"""usado p dar saltos p partes distantes do codigo"""
################## CLASSE TIPO-S #############################
class TipoS:
    def __init__(self, rs1, rs2, opcode, funct3, imm):
        self.rs1 = f"{rs1:05b}"
        self.rs2 = f"{rs2:05b}"
        self.opcode = f"{opcode:07b}"
        self.funct3 = f"{funct3:03b}"
        imm_bin = f"{imm & 0xFFF:012b}"
        self.imm4_0 = imm_bin[7:]
        self.imm11_5 = imm_bin[:7]

    def montar(self):
        return self.rs1 + self.rs2 + self.opcode + self.funct3 + self.imm4_0 + self.imm11_5

"""salvar dados na memoria"""
################## CLASSE TIPO-B #############################
class TipoB:
    def __init__(self, rs1, rs2, opcode, funct3, imm):
        self.rs1 = f"{rs1:05b}"
        self.rs2 = f"{rs2:05b}"
        self.opcode = f"{opcode:07b}"
        self.funct3 = f"{funct3:03b}"
        imm_bin = f"{imm & 0x1FFF:013b}"
        self.imm4_1 = imm_bin[8:12]
        self.imm11 = imm_bin[1]
        self.imm12 = imm_bin[0]
        self.imm10_5 = imm_bin[2:8]

    def montar(self):
        return self.rs1 + self.rs2 + self.opcode + self.funct3 + self.imm4_1 + self.imm11 + self.im12 + self.imm10_5

"""tipo um if, se for verdadeiro, da um salto curto de codigo"""
###################### MAIN ###################################
print("Olá, você está em um simulador do RARS\n")

# nome_arquivo = input("Digite o nome do arquivo de extesão .asm para ser 'montado':")

nome_arquivo = "exemplo-lab1"
caminho_asm = entrada_arquivo(nome_arquivo)

if caminho_asm:
    conteudo_original = ler_arquivo(caminho_asm)
    conteudo_limpo = tratar_ws(conteudo_original)
    obj_arquivo_temp = cria_arquivo_temp(nome_arquivo)
    print(obj_arquivo_temp)
    
    try:
        alterar_arquivo_temp(conteudo_limpo, obj_arquivo_temp)
        nome_temp = obj_arquivo_temp.name
        print(nome_temp)
        obj_arquivo_temp.close() 
        executa_codigo(nome_temp)
    except:
        print("Alguma coisa de errado não está certa")
    finally:
        os.unlink(nome_temp)
        pass

################# IDEIAS SOBRE O CÓDIGO

"""
A memória RAM  pode ser uma tabela hash em que geramos o endereço em hexadecimal como a chave e colocamos o conteúdo como valor;

Se quisermos ser rígidos com os caracteres de entrada do arquivo lido, podemos mudar o tipo de encoding para 'ascii' assim, qualquer caracter que não for ascii
gerará uma exceção, o que poder ser bom, para retornarmos uma mensagem para o usuário.

Eu estou pengando um arquivo em .asm e lendo ele como se fosse .txt, existe algum erro possível nisso ?


arquivo.flush()
re.sub(r'#.*', '', linha).strip()        
re.sub(r'\s+', ' ', linha_limpa)
"""


