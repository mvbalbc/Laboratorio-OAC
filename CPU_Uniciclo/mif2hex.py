#!/usr/bin/env python3
# mif2hex.py - Converte arquivos .mif (Quartus) para .hex ($readmemh)
#
# Uso:
#   python mif2hex.py <entrada.mif> <saida.hex>
#
# Exemplos:
#   python mif2hex.py UnicicloInst.mif UnicicloInst.hex
#   python mif2hex.py UnicicloData.mif UnicicloData.hex
#
# O arquivo .hex gerado contém um valor hexadecimal de 32 bits por linha,
# compativel com $readmemh do Verilog.

import sys
import re


def mif_to_hex(input_path, output_path):
    with open(input_path, "r") as f:
        lines = f.readlines()

    in_content = False
    values = []

    for line in lines:
        stripped = line.strip()

        if stripped.upper().startswith("BEGIN"):
            in_content = True
            continue

        if stripped.upper().startswith("END;"):
            in_content = False
            continue

        if not in_content:
            continue

        stripped = stripped.rstrip(";").strip()
        if not stripped:
            continue

        # Formato esperado: ADDR : DATA ;
        match = re.match(r"[0-9a-fA-F]+\s*:\s*([0-9a-fA-F]+)", stripped)
        if match:
            values.append(match.group(1).upper().zfill(8))

    with open(output_path, "w") as f:
        for val in values:
            f.write(val + "\n")

    print(f"Convertido: {input_path} -> {output_path} ({len(values)} palavras)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python mif2hex.py <entrada.mif> <saida.hex>")
        sys.exit(1)
    mif_to_hex(sys.argv[1], sys.argv[2])
