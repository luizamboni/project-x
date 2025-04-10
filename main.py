import argparse
import logging
from visa_mcc_module import EDIParser, aplicar_regra_por_descricao

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def processar_arquivo(path_arquivo, taxas):
    logging.info("Iniciando processamento do arquivo EDI")
    parser = EDIParser(path_arquivo)
    parser.parse()
    logging.info("Parsing concluído. Iniciando análise de registros...")

    total_linhas = 0

    for registro in parser.records:
        total_linhas += 1
        mcc = registro.get("mcc", "").strip()

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
        logging.debug(f"Processando registro {total_linhas}: MCC={mcc}")
        logging.debug(f"Processando registro {total_linhas}: ID={id_transacao}, MCC={mcc}, valor_autorizado={valor_autorizado}, valor_final={valor_final}")

        resultado = aplicar_regra_por_descricao(mcc, valor_autorizado, valor_final, taxas)
        valor_esperado = resultado.get("valor_final")
        if resultado["status"] == "sucesso" and abs(valor_esperado - valor_final) < 0.01:
            status_comparacao = "✓ valor final compatível"
        elif resultado["status"] == "sucesso":
            status_comparacao = f"⚠ valor divergente (esperado: {valor_esperado}, encontrado: {valor_final})"
        else:
            status_comparacao = f"✗ {resultado['mensagem']}"

        print(f"{id_transacao}: {resultado['status']} - {status_comparacao}")
        print()

    logging.info(f"Total de registros processados: {total_linhas}")


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