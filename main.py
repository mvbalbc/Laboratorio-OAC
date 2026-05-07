import math

# -----------------------------------------------------------------------------
# 1. ESTRUTURA DE DADOS: [Nome, ABI, Descrição, Salvo por, VALOR]
# -----------------------------------------------------------------------------
# Registradores x0-x31 (Inteiros) e f0-f31 (Ponto Flutuante)
registradores = [
    # Inteiros (Iniciam com 0)
    ["x0",  "zero", "Constante zero", "N/A", 0],
    ["x1",  "ra",   "Return Address", "Caller", 0],
    ["x2",  "sp",   "Stack Pointer",  "Callee", 0],
    ["x3",  "gp",   "Global Pointer", "N/A", 0],
    ["x4",  "tp",   "Thread Pointer", "N/A", 0],
    ["x5",  "t0",   "Temporário 0",    "Caller", 0],
    ["x6",  "t1",   "Temporário 1",    "Caller", 0],
    ["x7",  "t2",   "Temporário 2",    "Caller", 0],
    ["x8",  "s0",   "Frame Pointer",  "Callee", 0],
    ["x9",  "s1",   "Salvo 1",         "Callee", 0],
    ["x10", "a0",   "Arg 0 / Retorno", "Caller", 0],
    ["x11", "a1",   "Arg 1 / Retorno", "Caller", 0],
    ["x12", "a2",   "Argumento 2",     "Caller", 0],
    ["x13", "a3",   "Argumento 3",     "Caller", 0],
    ["x14", "a4",   "Argumento 4",     "Caller", 0],
    ["x15", "a5",   "Argumento 5",     "Caller", 0],
    ["x16", "a6",   "Argumento 6",     "Caller", 0],
    ["x17", "a7",   "Argumento 7",     "Caller", 0],
    ["x18", "s2",   "Salvo 2",         "Callee", 0],
    ["x19", "s3",   "Salvo 3",         "Callee", 0],
    ["x20", "s4",   "Salvo 4",         "Callee", 0],
    ["x21", "s5",   "Salvo 5",         "Callee", 0],
    ["x22", "s6",   "Salvo 6",         "Callee", 0],
    ["x23", "s7",   "Salvo 7",         "Callee", 0],
    ["x24", "s8",   "Salvo 8",         "Callee", 0],
    ["x25", "s9",   "Salvo 9",         "Callee", 0],
    ["x26", "s10",  "Salvo 10",        "Callee", 0],
    ["x27", "s11",  "Salvo 11",        "Callee", 0],
    ["x28", "t3",   "Temporário 3",    "Caller", 0],
    ["x29", "t4",   "Temporário 4",    "Caller", 0],
    ["x30", "t5",   "Temporário 5",    "Caller", 0],
    ["x31", "t6",   "Temporário 6",    "Caller", 0],
    
    # Ponto Flutuante (Iniciam com 0.0)
    ["f0",  "ft0",  "FP Temp 0",       "Caller", 0.0],
    ["f1",  "ft1",  "FP Temp 1",       "Caller", 0.0],
    ["f2",  "ft2",  "FP Temp 2",       "Caller", 0.0],
    ["f3",  "ft3",  "FP Temp 3",       "Caller", 0.0],
    ["f4",  "ft4",  "FP Temp 4",       "Caller", 0.0],
    ["f5",  "ft5",  "FP Temp 5",       "Caller", 0.0],
    ["f6",  "ft6",  "FP Temp 6",       "Caller", 0.0],
    ["f7",  "ft7",  "FP Temp 7",       "Caller", 0.0],
    ["f8",  "fs0",  "FP Salvo 0",      "Callee", 0.0],
    ["f9",  "fs1",  "FP Salvo 1",      "Callee", 0.0],
    ["f10", "fa0",  "FP Arg 0 / Ret",  "Caller", 0.0],
    ["f11", "fa1",  "FP Arg 1 / Ret",  "Caller", 0.0],
    ["f12", "fa2",  "FP Arg 2",        "Caller", 0.0],
    ["f13", "fa3",  "FP Arg 3",        "Caller", 0.0],
    ["f14", "fa4",  "FP Arg 4",        "Caller", 0.0],
    ["f15", "fa5",  "FP Arg 5",        "Caller", 0.0],
    ["f16", "fa6",  "FP Arg 6",        "Caller", 0.0],
    ["f17", "fa7",  "FP Arg 7",        "Caller", 0.0],
    ["f18", "fs2",  "FP Salvo 2",      "Callee", 0.0],
    ["f19", "fs3",  "FP Salvo 3",      "Callee", 0.0],
    ["f20", "fs4",  "FP Salvo 4",      "Callee", 0.0],
    ["f21", "fs5",  "FP Salvo 5",      "Callee", 0.0],
    ["f22", "fs6",  "FP Salvo 6",      "Callee", 0.0],
    ["f23", "fs7",  "FP Salvo 7",      "Callee", 0.0],
    ["f24", "fs8",  "FP Salvo 8",      "Callee", 0.0],
    ["f25", "fs9",  "FP Salvo 9",      "Callee", 0.0],
    ["f26", "fs10", "FP Salvo 10",     "Callee", 0.0],
    ["f27", "fs11", "FP Salvo 11",     "Callee", 0.0],
    ["f28", "ft8",  "FP Temp 8",       "Caller", 0.0],
    ["f29", "ft9",  "FP Temp 9",       "Caller", 0.0],
    ["f30", "ft10", "FP Temp 10",      "Caller", 0.0],
    ["f31", "ft11", "FP Temp 11",      "Caller", 0.0]
]

# -----------------------------------------------------------------------------
# 2. FUNÇÕES DE SUPORTE
# -----------------------------------------------------------------------------

def get_reg_idx(nome):
    """Retorna o índice na lista 'registradores' baseado no nome xN ou ABI."""
    nome = nome.lower().strip()
    for i, reg in enumerate(registradores):
        if reg[0] == nome or reg[1] == nome:
            return i
    raise ValueError(f"Registrador '{nome}' não existe.")

def limpar_linhas(linhas):
    """Remove comentários, vírgulas e organiza as partes da instrução."""
    instrucoes_limpas = []
    for linha in linhas:
        # Remove comentários (#) e espaços extras
        processada = linha.split("#")[0].strip()
        if not processada:
            continue
        
        # Substitui vírgulas por espaços e separa os termos
        partes = processada.replace(",", " ").split()
        instrucoes_limpas.append(partes)
    return instrucoes_limpas

# -----------------------------------------------------------------------------
# 3. MOTOR DE EXECUÇÃO (MATCH-CASE)
# -----------------------------------------------------------------------------

def executar_Instrucoes(lista_inst):
    for inst in lista_inst:
        op = inst[0].lower()
        
        try:
            # Rd é quase sempre o primeiro argumento após o opcode
            rd_idx = get_reg_idx(inst[1])
            
            # x0 é imutável (Hardwired zero)
            if rd_idx == 0: continue

            match op:
                # --- INTEIROS: ARITMÉTICA R-TYPE (Rd, Rs1, Rs2) ---
                case "add":
                    v1 = registradores[get_reg_idx(inst[2])][4]
                    v2 = registradores[get_reg_idx(inst[3])][4]
                    registradores[rd_idx][4] = (v1 + v2) & 0xFFFFFFFF
                case "sub":
                    v1 = registradores[get_reg_idx(inst[2])][4]
                    v2 = registradores[get_reg_idx(inst[3])][4]
                    registradores[rd_idx][4] = (v1 - v2) & 0xFFFFFFFF
                case "and":
                    v1 = registradores[get_reg_idx(inst[2])][4]
                    v2 = registradores[get_reg_idx(inst[3])][4]
                    registradores[rd_idx][4] = v1 & v2
                case "or":
                    v1 = registradores[get_reg_idx(inst[2])][4]
                    v2 = registradores[get_reg_idx(inst[3])][4]
                    registradores[rd_idx][4] = v1 | v2
                case "xor":
                    v1 = registradores[get_reg_idx(inst[2])][4]
                    v2 = registradores[get_reg_idx(inst[3])][4]
                    registradores[rd_idx][4] = v1 ^ v2

                # --- INTEIROS: IMEDIATOS I-TYPE (Rd, Rs1, Imm) ---
                case "addi":
                    v1 = registradores[get_reg_idx(inst[2])][4]
                    imm = int(inst[3])
                    registradores[rd_idx][4] = (v1 + imm) & 0xFFFFFFFF
                case "andi":
                    v1 = registradores[get_reg_idx(inst[2])][4]
                    imm = int(inst[3])
                    registradores[rd_idx][4] = v1 & imm
                case "li": # Pseudo-instrução Load Immediate
                    registradores[rd_idx][4] = int(inst[2]) & 0xFFFFFFFF

                # --- EXTENSÃO M: MULTIPLICAÇÃO/DIVISÃO ---
                case "mul":
                    v1 = registradores[get_reg_idx(inst[2])][4]
                    v2 = registradores[get_reg_idx(inst[3])][4]
                    registradores[rd_idx][4] = (v1 * v2) & 0xFFFFFFFF
                case "div":
                    v1 = registradores[get_reg_idx(inst[2])][4]
                    v2 = registradores[get_reg_idx(inst[3])][4]
                    registradores[rd_idx][4] = (v1 // v2) if v2 != 0 else 0

                # --- PONTO FLUTUANTE: RV32F (frd, frs1, frs2) ---
                case "fadd.s":
                    f1 = registradores[get_reg_idx(inst[2])][4]
                    f2 = registradores[get_reg_idx(inst[3])][4]
                    registradores[rd_idx][4] = float(f1 + f2)
                case "fsub.s":
                    f1 = registradores[get_reg_idx(inst[2])][4]
                    f2 = registradores[get_reg_idx(inst[3])][4]
                    registradores[rd_idx][4] = float(f1 - f2)
                case "fmul.s":
                    f1 = registradores[get_reg_idx(inst[2])][4]
                    f2 = registradores[get_reg_idx(inst[3])][4]
                    registradores[rd_idx][4] = float(f1 * f2)
                case "fdiv.s":
                    f1 = registradores[get_reg_idx(inst[2])][4]
                    f2 = registradores[get_reg_idx(inst[3])][4]
                    registradores[rd_idx][4] = float(f1 / f2) if f2 != 0 else float('inf')
                
                # --- CONVERSÕES ---
                case "fcvt.s.w": # Int para Float
                    val_int = registradores[get_reg_idx(inst[2])][4]
                    registradores[rd_idx][4] = float(val_int)
                case "fcvt.w.s": # Float para Int
                    val_float = registradores[get_reg_idx(inst[2])][4]
                    registradores[rd_idx][4] = int(val_float) & 0xFFFFFFFF

                case _:
                    print(f"Instrução '{op}' não implementada ou não reconhecida.")

        except Exception as e:
            print(f"Erro ao processar '{inst}': {e}")

# -----------------------------------------------------------------------------
# 4. EXECUÇÃO DE EXEMPLO
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # Simulando um código assembly RISC-V
    codigo_exemplo = [
        "addi a0, zero, 20      # Carrega 20 em a0",
        "li t0, 5               # t0 = 5 (usando li)",
        "mul a1, a0, t0         # a1 = 20 * 5 = 100",
        "fcvt.s.w ft0, a1       # Converte 100 para float em ft0",
        "fadd.s fa0, ft0, ft0   # fa0 = 100.0 + 100.0 = 200.0",
        "sub x0, a0, a1         # Tentativa de escrita no zero (deve ser ignorada)"
    ]

    print("--- Iniciando Simulação ---")
    insts = limpar_linhas(codigo_exemplo)
    executar_Instrucoes(insts)

    print("\n--- Estado Final dos Registradores Alterados ---")
    print(f"{'Reg':<5} | {'ABI':<5} | {'Valor':<10} | {'Tipo'}")
    print("-" * 35)
    for r in registradores:
        if r[4] != 0 and r[4] != 0.0:
            tipo = "Float" if isinstance(r[4], float) else "Int"
            print(f"{r[0]:<5} | {r[1]:<5} | {r[4]:<10} | {tipo}")