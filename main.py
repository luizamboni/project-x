import argparse
import csv
from visa_mcc_module import aplicar_regra_por_descricao

def processar_arquivo(path_arquivo, taxas):
    with open(path_arquivo, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="|")
        for linha in reader:
            descricao = linha["Descrição MCC"]
            valor_autorizado = float(linha["Valor Autorizado (R$)"])
            valor_final = float(linha["Valor Final (R$)"])
            id_transacao = linha["ID Transação"]

            resultado = aplicar_regra_por_descricao(descricao, valor_autorizado, valor_final, taxas)
            valor_esperado = resultado.get("valor_final")

            if resultado["status"] == "sucesso" and abs(valor_esperado - valor_final) < 0.01:
                status_comparacao = "✓ valor final compatível"
            elif resultado["status"] == "sucesso":
                status_comparacao = f"⚠ valor divergente (esperado: {valor_esperado}, encontrado: {valor_final})"
            else:
                status_comparacao = f"✗ {resultado['mensagem']}"

            print(f"{id_transacao}: {resultado['status']} - {status_comparacao}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Processa transações Visa por MCC.")
    parser.add_argument("arquivo", help="Caminho para o arquivo .adi de transações")
    parser.add_argument("--irf", type=float, default=0.015)
    parser.add_argument("--bandeira", type=float, default=0.005)
    parser.add_argument("--adquirente", type=float, default=0.005)
    parser.add_argument("--subadquirente", type=float, default=0.005)

    args = parser.parse_args()

    taxas = {
        "irf": args.irf,
        "bandeira": args.bandeira,
        "adquirente": args.adquirente,
        "subadquirente": args.subadquirente,
    }

    processar_arquivo(args.arquivo, taxas)
