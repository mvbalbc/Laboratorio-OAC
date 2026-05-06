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
            if linha:
                pass
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


###################### MAIN ###################################
print("Olá, você está em um simulador do RARS\n")

# nome_arquivo = input("Digite o nome do arquivo de extesão .asm para ser 'montado':")

nome_arquivo = "exemplo-lab1"
caminho_asm = entrada_arquivo(nome_arquivo)

if caminho_asm:
    conteudo_original = ler_arquivo(caminho_asm)
    conteudo_limpo = tratar_ws(conteudo_original)
    temp_file_obj = cria_arquivo_temp(nome_arquivo)
    print(temp_file_obj)
    
    try:
        alterar_arquivo_temp(conteudo_limpo, temp_file_obj)
        nome_temp = temp_file_obj.name
        print(nome_temp)
        temp_file_obj.close() 
        executa_codigo(nome_temp)
    except:
        print("Alguma coisa de errado não deu certo")
    finally:
        #os.unlink(nome_temp)
        pass


################# IDEIAS SOBRE O CÓDIGO

"""
A memória RAM  pode ser uma tabela hash em que geramos o endereço em hexadecimal como a chave e colocamos o conteúdo como valor;

Se quisermos ser rígidos com os caracteres de entrada do arquivo lido, podemos mudar o tipo de encoding para 'ascii' assim, qualquer caracter que não for ascii
gerará uma exceção, o que poder ser bom, para retornarmos uma mensagem para o usuário.

Eu estou pengando um arquivo em .asm e lendo ele como se fosse .txt, existe algum erro possível nisso ?

"""


