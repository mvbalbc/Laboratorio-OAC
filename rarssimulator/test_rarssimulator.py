import pytest
import os
from pathlib import Path
from main import tratar_ws, entrada_arquivo

# 1. Teste de Sanatização (Garante que o parser do Assembly não pegue lixo)
def test_tratar_ws_limpeza_profunda():
    entrada = ["  add t0, t1, t2  ", "\n", "  # comentário", "sub a0, a1, x0"]
    # Nota: Seu código atual mantém '#' se não houver filtro de comentários
    resultado = tratar_ws(entrada)
    assert "addt0,t1,t2" in resultado
    assert "" not in resultado # Garante que removeu linhas vazias

# 2. Teste de Localização de Arquivo
def test_entrada_arquivo_validacao(tmp_path):
    # Cria um arquivo fictício para o teste
    d = tmp_path / "projeto"
    d.mkdir()
    f = d / "teste.asm"
    f.write_text("add t0, t1, t2")
    
    os.chdir(d) # Move o contexto do teste para a pasta temporária
    assert entrada_arquivo("teste") == "teste.asm"

# 3. Teste de Falha (Arquivo Inexistente)
def test_entrada_arquivo_inexistente():
    assert entrada_arquivo("arquivo_fantasma") is None

# 4. Teste de Persistência no Arquivo Temporário
def test_escrita_arquivo_temporario(tmp_path):
    from main import cria_arquivo_temp, alterar_arquivo_temp
    
    temp = cria_arquivo_temp("teste")
    conteudo = "addit0,x0,10"
    alterar_arquivo_temp(conteudo, temp)
    temp.seek(0)
    assert temp.read() == conteudo
    temp.close()
    os.unlink(temp.name)