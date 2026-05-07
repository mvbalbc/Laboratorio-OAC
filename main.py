riscv_32_registers = [
    # --- Registradores de Propósito Geral (Inteiros) ---
    ["x0",  "zero", "Constante zero (sempre 0)",          "N/A"],
    ["x1",  "ra",   "Endereço de retorno (Return Address)", "Caller"],
    ["x2",  "sp",   "Ponteiro de Pilha (Stack Pointer)",    "Callee"],
    ["x3",  "gp",   "Ponteiro Global (Global Pointer)",     "N/A"],
    ["x4",  "tp",   "Ponteiro de Thread (Thread Pointer)",  "N/A"],
    ["x5",  "t0",   "Temporário 0",                         "Caller"],
    ["x6",  "t1",   "Temporário 1",                         "Caller"],
    ["x7",  "t2",   "Temporário 2",                         "Caller"],
    ["x8",  "s0/fp","Registrador Salvo 0 / Frame Pointer", "Callee"],
    ["x9",  "s1",   "Registrador Salvo 1",                  "Callee"],
    ["x10", "a0",   "Argumento 0 / Valor de Retorno",       "Caller"],
    ["x11", "a1",   "Argumento 1 / Valor de Retorno",       "Caller"],
    ["x12", "a2",   "Argumento 2",                          "Caller"],
    ["x13", "a3",   "Argumento 3",                          "Caller"],
    ["x14", "a4",   "Argumento 4",                          "Caller"],
    ["x15", "a5",   "Argumento 5",                          "Caller"],
    ["x16", "a6",   "Argumento 6",                          "Caller"],
    ["x17", "a7",   "Argumento 7",                          "Caller"],
    ["x18", "s2",   "Registrador Salvo 2",                  "Callee"],
    ["x19", "s3",   "Registrador Salvo 3",                  "Callee"],
    ["x20", "s4",   "Registrador Salvo 4",                  "Callee"],
    ["x21", "s5",   "Registrador Salvo 5",                  "Callee"],
    ["x22", "s6",   "Registrador Salvo 6",                  "Callee"],
    ["x23", "s7",   "Registrador Salvo 7",                  "Callee"],
    ["x24", "s8",   "Registrador Salvo 8",                  "Callee"],
    ["x25", "s9",   "Registrador Salvo 9",                  "Callee"],
    ["x26", "s10",  "Registrador Salvo 10",                 "Callee"],
    ["x27", "s11",  "Registrador Salvo 11",                 "Callee"],
    ["x28", "t3",   "Temporário 3",                         "Caller"],
    ["x29", "t4",   "Temporário 4",                         "Caller"],
    ["x30", "t5",   "Temporário 5",                         "Caller"],
    ["x31", "t6",   "Temporário 6",                         "Caller"],

    # --- Registradores de Ponto Flutuante (Floating-Point) ---
    ["f0",  "ft0",  "FP Temporário 0",                      "Caller"],
    ["f1",  "ft1",  "FP Temporário 1",                      "Caller"],
    ["f2",  "ft2",  "FP Temporário 2",                      "Caller"],
    ["f3",  "ft3",  "FP Temporário 3",                      "Caller"],
    ["f4",  "ft4",  "FP Temporário 4",                      "Caller"],
    ["f5",  "ft5",  "FP Temporário 5",                      "Caller"],
    ["f6",  "ft6",  "FP Temporário 6",                      "Caller"],
    ["f7",  "ft7",  "FP Temporário 7",                      "Caller"],
    ["f8",  "fs0",  "FP Salvo 0",                           "Callee"],
    ["f9",  "fs1",  "FP Salvo 1",                           "Callee"],
    ["f10", "fa0",  "FP Argumento 0 / Retorno",             "Caller"],
    ["f11", "fa1",  "FP Argumento 1 / Retorno",             "Caller"],
    ["f12", "fa2",  "FP Argumento 2",                       "Caller"],
    ["f13", "fa3",  "FP Argumento 3",                       "Caller"],
    ["f14", "fa4",  "FP Argumento 4",                       "Caller"],
    ["f15", "fa5",  "FP Argumento 5",                       "Caller"],
    ["f16", "fa6",  "FP Argumento 6",                       "Caller"],
    ["f17", "fa7",  "FP Argumento 7",                       "Caller"],
    ["f18", "fs2",  "FP Salvo 2",                           "Callee"],
    ["f19", "fs3",  "FP Salvo 3",                           "Callee"],
    ["f20", "fs4",  "FP Salvo 4",                           "Callee"],
    ["f21", "fs5",  "FP Salvo 5",                           "Callee"],
    ["f22", "fs6",  "FP Salvo 6",                           "Callee"],
    ["f23", "fs7",  "FP Salvo 7",                           "Callee"],
    ["f24", "fs8",  "FP Salvo 8",                           "Callee"],
    ["f25", "fs9",  "FP Salvo 9",                           "Callee"],
    ["f26", "fs10", "FP Salvo 10",                          "Callee"],
    ["f27", "fs11", "FP Salvo 11",                          "Callee"],
    ["f28", "ft8",  "FP Temporário 8",                      "Caller"],
    ["f29", "ft9",  "FP Temporário 9",                      "Caller"],
    ["f30", "ft10", "FP Temporário 10",                     "Caller"],
    ["f31", "ft11", "FP Temporário 11",                     "Caller"],

    # --- Registradores Especiais (CSRs comuns) ---
    ["pc",   "pc",    "Contador de Programa (Instrução atual)", "N/A"],
    ["fcsr", "fcsr",  "Controle/Status de Ponto Flutuante",     "N/A"]
]

# Exemplo de como acessar:
# for reg in riscv_32_registers:
#     print(f"Registrador: {reg[0]} | ABI: {reg[1]} | Função: {reg[2]}")

def ler_arquivo (caminho):
    with open(caminho, 'r') as programa:
        return programa.readlines()
    
def limpar_linhas (arquivo):
    instrucoes = []
    for linha in arquivo:
        linha_limpa = linha.strip()
        linha_limpa = linha_limpa.split("#")[0]
        linha_limpa = linha_limpa.replace(",", " ")

        if ((not linha_limpa) or (linha_limpa[0] == "#")):
            continue

        linha_limpa = linha_limpa.strip()
        if len(linha_limpa) == 4:
            instrucao = linha_limpa[0].lower()
            rd = linha_limpa[1]
            rs1 = linha_limpa[2]
            rs2 = linha_limpa[3]
            instrucoes.append([instrucao, rd, rs1, rs2])

    return instrucoes

def ler_Instrucoes (lista):
    try:
        for instrucao in lista:
            
            # Regra de Ouro: Escritas no x0 (zero) são sempre ignoradas
                if instrucao[1] == 0 and instrucao[0] not in ["fadd.s", "fsub.s", "fmul.s"]: # Simplificação
                    if not instrucao[0].startswith("f"): # Se for registrador inteiro
                        return
                
                match instrucao[0]:
                    # --- ARITMÉTICA E LÓGICA (R-TYPE) ---
                    case "add":
                        regs_int[rd] = (rs1_val + rs2_val) & 0xFFFFFFFF
                    case "sub":
                        regs_int[rd] = (rs1_val - rs2_val) & 0xFFFFFFFF
                    case "sll": # Shift Left Logical
                        regs_int[rd] = (rs1_val << (rs2_val & 0x1F)) & 0xFFFFFFFF
                    case "srl": # Shift Right Logical
                        regs_int[rd] = (rs1_val >> (rs2_val & 0x1F)) & 0xFFFFFFFF
                    case "sra": # Shift Right Arithmetic
                        regs_int[rd] = (rs1_val >> (rs2_val & 0x1F)) # Python trata sinal em int
                    case "and":
                        regs_int[rd] = rs1_val & rs2_val
                    case "or":
                        regs_int[rd] = rs1_val | rs2_val
                    case "xor":
                        regs_int[rd] = rs1_val ^ rs2_val
                    case "slt": # Set Less Than (Signed)
                        regs_int[rd] = 1 if rs1_val < rs2_val else 0

                    # --- ARITMÉTICA COM IMEDIATOS (I-TYPE) ---
                    case "addi":
                        regs_int[rd] = (rs1_val + imm) & 0xFFFFFFFF
                    case "slli":
                        regs_int[rd] = (rs1_val << imm) & 0xFFFFFFFF
                    case "srli":
                        regs_int[rd] = (rs1_val >> imm) & 0xFFFFFFFF
                    case "andi":
                        regs_int[rd] = rs1_val & imm
                    case "ori":
                        regs_int[rd] = rs1_val | imm

                    # --- CARREGAMENTO DE MEMÓRIA (LOADS) ---
                    case "lw": # Load Word
                        # O valor viria da memória: Mem[rs1 + imm]
                        regs_int[rd] = rs1_val # Representação simplificada
                    case "lui": # Load Upper Immediate
                        regs_int[rd] = (imm << 12) & 0xFFFFFFFF

                    # --- EXTENSÃO M (MULTIPLICAÇÃO/DIVISÃO) ---
                    case "mul":
                        regs_int[rd] = (rs1_val * rs2_val) & 0xFFFFFFFF
                    case "div":
                        regs_int[rd] = (rs1_val // rs2_val) if rs2_val != 0 else -1
                    case "rem":
                        regs_int[rd] = (rs1_val % rs2_val) if rs2_val != 0 else rs1_val

                    # --- PONTO FLUTUANTE (RV32F) ---
                    case "fadd.s":
                        regs_fp[rd] = rs1_val + rs2_val
                    case "fsub.s":
                        regs_fp[rd] = rs1_val - rs2_val
                    case "fmul.s":
                        regs_fp[rd] = rs1_val * rs2_val
                    case "fdiv.s":
                        regs_fp[rd] = rs1_val / rs2_val if rs2_val != 0 else float('inf')
                    case "fcvt.s.w": # Converte Inteiro para Float
                        regs_fp[rd] = float(rs1_val)
                    case "fcvt.w.s": # Converte Float para Inteiro
                        regs_int[rd] = int(rs1_val) & 0xFFFFFFFF

                    case _:
                        print(f"Instrução {instrucao} não reconhecida.")
    except Exception as e:
        print(f"Erro ao ler instruções: {e}")
    return





if __name__ == "__main__":
    print()
