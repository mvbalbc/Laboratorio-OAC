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
            print(f'Preparando para ler o arquivo')
            cria_arquivo_temp(nome_completo_arquivo)
        else:
            print(f"O nome do arquivo não foi encontrado")
            print(arquivos_asm)

    else:
        print(f"Nenhum arquivo .asm foi encontrado.")


##################### LEITURA DE ARQUIVO #######################

def ler_arquivo(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.readlines()
    return conteudo

##################### ANALISE DO ARQUIVO #######################

def analisar_arquivo(nome_arquivo):
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                if linha:
                     """
                     Será que é necessário separar o .text do .data ?
                     """

#################### TRATAMENTO DO CONTEUDO DO ARQUIVO ########

def tratar_ws(linhas_arquivo):
    linhas_tratadas = [linha.lstrip().replace(" ", "") for linha in linhas_arquivo if linha]
    return linhas_tratadas


#################### CRIACAO DO ARQUIVO TEMPORARIO ############

def cria_arquivo_temp(nome_arquivo):
    conteudo = ler_arquivo(nome_arquivo)
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as arquivo_temp:
        arquivo_temp.write(str(conteudo))
        arquivo_temp.seek(0)
    alterar_arquivo(conteudo)


################### ALTERAR O ARQUIVO TEMPORARIO #############
 
def alterar_arquivo(linhas_arquivo):
    arquivo_sem_ws = tratar_ws(linhas_arquivo)
    print("alterando o arquivo")
    print(arquivo_sem_ws)



###################### MAIN ###################################
print("Olá, você está em um simulador do RARS\n")

# nome_arquivo = input("Digite o nome do arquivo de extesão .asm para ser 'montado':")

entrada_arquivo("exemplo-lab1")


