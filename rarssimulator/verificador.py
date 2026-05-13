import subprocess
import os
import sys
import argparse

# ================= CONFIGURAÇÕES =================
NOME_RARS = "rars.jar" 
COMANDO_ASSEMBLER = "main.py" 
# =================================================

def rodar_comando(comando, descricao):
    print(f"⏳ Rodando {descricao}...")
    try:
        subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ {descricao} concluído.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao rodar {descricao}.")
        print("\n--- SAÍDA DO ERRO ---")
        print(e.stdout.decode('utf-8', errors='ignore'))
        print(e.stderr.decode('utf-8', errors='ignore'))
        print("---------------------\n")
        sys.exit(1)

def extrair_dados_mif(caminho_arquivo):
    valores = []
    if not os.path.exists(caminho_arquivo):
        return valores
        
    with open(caminho_arquivo, 'r') as f:
        dentro_content = False
        for linha in f:
            linha = linha.strip()
            if linha == "BEGIN":
                dentro_content = True
                continue
            if linha == "END;":
                break
            if dentro_content and ':' in linha:
                valor = linha.split(':')[1].strip().replace(';', '')
                valores.append(valor)
    return valores

def extrair_dados_rars(caminho_arquivo):
    valores = []
    if not os.path.exists(caminho_arquivo):
         return valores
         
    with open(caminho_arquivo, 'r') as f:
        for linha in f:
            valor = linha.strip()
            if valor:
                valores.append(valor)
    return valores

def comparar_secoes(nome_secao, valores_mif, valores_rars):
    print(f"\n🔍 Comparando seção {nome_secao} linha a linha...")
    
    # Se ambos estiverem vazios, não tem o que comparar
    if not valores_mif and not valores_rars:
        print(f"⚠️ Seção {nome_secao} vazia em ambos os arquivos.")
        return

    # Se um existir e o outro não
    if not valores_mif or not valores_rars:
        print(f"⚠️ Pulo da seção {nome_secao}: Faltando dados do MIF ou do RARS.")
        return

    tamanho_max = max(len(valores_mif), len(valores_rars))
    mif_pad = valores_mif + ['00000000'] * (tamanho_max - len(valores_mif))
    rars_pad = valores_rars + ['00000000'] * (tamanho_max - len(valores_rars))
    
    erros = 0
    print("-" * 65)
    print(f"{'ENDEREÇO':<12} | {'RARS (GABARITO)':<18} | {'SEU ASSEMBLER (.MIF)':<20} | STATUS")
    print("-" * 65)
    
    for i in range(tamanho_max):
        endereco_hex = f"{i*4:04x}"
        rars_val = rars_pad[i]
        mif_val = mif_pad[i]
        
        if mif_val == rars_val:
            print(f"0x{endereco_hex:<10} | {rars_val:<18} | {mif_val:<20} | ✅ OK")
        else:
            print(f"0x{endereco_hex:<10} | {rars_val:<18} | {mif_val:<20} | ❌ ERRO")
            erros += 1
            
    print("-" * 65)
                
    if erros == 0:
        print(f"🎉 SUCESSO ABSOLUTO! A seção {nome_secao} bateu 100% com o RARS ({tamanho_max} linhas avaliadas)!")
    else:
        print(f"❌ FALHA! Foram encontradas {erros} divergência(s) na seção {nome_secao}.")

def main():
    parser = argparse.ArgumentParser(description="Verificador Automático de .mif contra o RARS.")
    parser.add_argument("arquivo_asm", help="Caminho do arquivo .asm (ex: exemplos/exemplo3.asm)")
    args = parser.parse_args()
    
    arquivo_alvo = args.arquivo_asm

    diretorio_alvo = os.path.dirname(arquivo_alvo)
    nome_base = os.path.splitext(os.path.basename(arquivo_alvo))[0]

    mif_text_esperado = os.path.join(diretorio_alvo, f"{nome_base}.text.mif")
    mif_data_esperado = os.path.join(diretorio_alvo, f"{nome_base}.data.mif")
    
    print(f"🚀 Iniciando Verificador para: {arquivo_alvo}")
    print(f"📌 Assembler configurado: {COMANDO_ASSEMBLER}")
    print(f"📌 Esperando gerar: {mif_text_esperado} e {mif_data_esperado}\n")

    # 1. Rodar o seu Assembler
    comando_assembler = ["python3", COMANDO_ASSEMBLER, arquivo_alvo]
    rodar_comando(comando_assembler, "Seu Assembler")

    # 2. Rodar o RARS localmente
    comando_rars = [
        "java", "-jar", NOME_RARS, "a", "nc",
        "dump", ".text", "HexText", "rars_text.txt",
        "dump", ".data", "HexText", "rars_data.txt",
        arquivo_alvo
    ]
    rodar_comando(comando_rars, "RARS (Golden Model)")

    # 3. Ler arquivos gerados
    mif_text = extrair_dados_mif(mif_text_esperado)
    mif_data = extrair_dados_mif(mif_data_esperado)
    rars_text = extrair_dados_rars("rars_text.txt")
    rars_data = extrair_dados_rars("rars_data.txt")

    if not mif_text and not mif_data:
        print(f"\n❌ ERRO FATAL: O verificador não achou os arquivos gerados.")
        print(f"Ele procurou por '{mif_text_esperado}' e '{mif_data_esperado}'.")
        print("Confirme se o assembler realmente concluiu a escrita!")
        sys.exit(1)

    # 4. Comparar (Agora com tabela completíssima)
    comparar_secoes(".text", mif_text, rars_text)
    comparar_secoes(".data", mif_data, rars_data)

    print("\n✅ Verificação concluída! Revise os resultados acima para detalhes.")
    print("\n Deseja apagar os arquivos criados pelo rars? rars_text.txt & rars_data.txt serão excluidos.")
    apagarounao = str(input("\nSIM ou NAO? \n"))


    while apagarounao not in ["SIM", "sim", "s", "S", "yes", "YES", "y", "Y", "NAO", "nao", "n", "N"]:
        print("Resposta inválida. Por favor, responda com SIM ou NAO.")
        apagarounao = str(input("\nSIM ou NAO? \n"))
    if apagarounao == "SIM" or apagarounao == "sim" or apagarounao == "s" or apagarounao == "sim" or apagarounao == "yes" or apagarounao == "y":

        try:
            os.remove("rars_text.txt")
            os.remove("rars_data.txt")
        except OSError:
            pass
    
        

if __name__ == "__main__":
    main()