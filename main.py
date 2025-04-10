import argparse
import logging
from visa_mcc_module import EDIParser, aplicar_regra_por_descricao
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def processar_arquivo(path_arquivo, taxas):
    logging.info("Iniciando processamento do arquivo EDI")
    parser = EDIParser(path_arquivo)
    parser.parse()
    logging.info("Parsing concluído. Iniciando análise de registros...")

    total_linhas = 0
    falhas_por_mcc = defaultdict(int)
    total_falhas = 0
    registros_por_mcc = defaultdict(int)
    motivos_por_mcc = defaultdict(list)

    for registro in parser.records:
        total_linhas += 1
        mcc = registro.get("mcc", "").strip()
        registros_por_mcc[mcc] += 1

        valor_autorizado = float(
            registro.get("valor_autorizado")
            or registro.get("Valor Autorizado (R$)")
            or registro.get("valor_bruto")
            or 0
        )

        valor_final = float(
            registro.get("valor_final")
            or registro.get("Valor Final (R$)")
            or registro.get("valor_liquido")
            or 0
        )

        id_transacao = registro.get("id") or registro.get("ID Transação") or registro.get("nsu_host")

        resultado = aplicar_regra_por_descricao(mcc, valor_autorizado, valor_final, taxas)
        valor_esperado = resultado.get("valor_final")
        if resultado["status"] == "sucesso" and abs(valor_esperado - valor_final) < 0.01:
            status_comparacao = "✓ valor final compatível"
        elif resultado["status"] == "sucesso":
            status_comparacao = f"⚠ valor divergente (esperado: {valor_esperado}, encontrado: {valor_final})"
        else:
            status_comparacao = f"✗ {resultado['mensagem']}"
            falhas_por_mcc[mcc] += 1
            total_falhas += 1
            motivos_por_mcc[mcc].append(resultado['mensagem'])

        if resultado["status"] != "sucesso":
            logging.debug(f"Processando registro {total_linhas}: MCC={mcc}")
            logging.debug(f"Processando registro {total_linhas}: ID={id_transacao}, MCC={mcc}, valor_autorizado={valor_autorizado}, valor_final={valor_final}")

            print(f"{id_transacao}: {resultado['status']} - {status_comparacao}")
            print()

    # Relatório final
    print("\nRelatório Final:")
    print(f"{'MCC':<15} {'Registros':<10} {'Falhas':<10} {'Motivo':<15}")
    for mcc, count in registros_por_mcc.items():
        falhas = falhas_por_mcc[mcc]
        motivo_comum = motivos_por_mcc[mcc][0] if motivos_por_mcc[mcc] else ""
        print(f"{mcc:<15} {count:<10} {falhas:<10} {motivo_comum:<15}")
    
    print(f"\nTotal de registros processados: {total_linhas}")
    print(f"Total de falhas: {total_falhas}")

    logging.info(f"Total de registros processados: {total_linhas}")
    logging.info(f"Total de falhas: {total_falhas}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Processa transações Visa por MCC via EDI.")
    parser.add_argument("arquivo", help="Caminho para o arquivo .edi de transações")
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