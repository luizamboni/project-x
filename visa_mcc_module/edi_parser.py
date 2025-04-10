import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class EDIParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.records = []

    def parse(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            for line in file:
                record_type = line[0:2]
                logging.debug(f"Lendo linha: {line.strip()}")
                if record_type == "A0":
                    self.records.append(self.parse_a0(line))
                elif record_type == "L0":
                    self.records.append(self.parse_l0(line))
                elif record_type == "CV":
                    self.records.append(self.parse_cv(line))
                elif record_type == "AJ":
                    self.records.append(self.parse_aj(line))
                elif record_type == "CC":
                    self.records.append(self.parse_cc(line))
                elif record_type == "L9":
                    self.records.append(self.parse_l9(line))
                elif record_type == "A9":
                    self.records.append(self.parse_a9(line))
                else:
                    logging.debug(f"Registro desconhecido: {record_type}")

    def parse_a0(self, line):
        return {
            "tipo": "A0",
            "versao_layout": line[2:8].strip(),
            "data_geracao": line[8:16],
            "hora_geracao": line[16:22],
            "id_movimento": line[22:28],
            "nome_adquirente": line[28:58].strip(),
            "provedor_servico": line[58:62].strip(),
            "codigo_estabelecimento": line[62:71].strip(),
            "tipo_processamento": line[71],
            "nseq": line[72:78],
        }

    def parse_l0(self, line):
        return {
            "tipo": "L0",
            "data_movimento": line[2:10],
            "moeda": line[10:12],
            "nseq": line[12:18],
        }

    def parse_cv(self, line):
        codigo_estabelecimento = line[2:17]
        # mcc_map = {
        #     "000000000012345": "5812",
        #     "000000000045678": "5813",
        #     "000000000078910": "5814",
        #     "000000000011122": "4511",
        #     "000000000033344": "4121",
        # }
        
        # mcc = mcc_map.get(codigo_estabelecimento, "0000")
        mcc = line[447:451]
        logging.debug(f"Código do estabelecimento: {codigo_estabelecimento}, MCC deduzido: {mcc}")
        return {
            "tipo": "CV",
            "codigo_estabelecimento": codigo_estabelecimento,
            "nsu_host": line[17:29],
            "data_transacao": line[29:37],
            "tipo_lancamento": line[43],
            "data_lancamento": line[44:52],
            "tipo_produto": line[52],
            "meio_captura": line[53],
            "valor_bruto": line[54:65],
            "valor_desconto": line[65:76],
            "valor_liquido": line[76:87],
            "mcc": mcc,
        }

    def parse_aj(self, line):
        return {
            "tipo": "AJ",
            "codigo_estabelecimento": line[2:17],
            "nsu_transacao_original": line[17:29],
            "data_transacao_original": line[29:37],
            "numero_parcela": line[37:39],
            "nsu_transacao_ajuste": line[39:51],
            "data_ajuste": line[51:59],
            "tipo_lancamento": line[65],
            "data_lancamento": line[66:74],
            "tipo_ajuste": line[75],
            "codigo_ajuste": line[76:79],
            "descricao_ajuste": line[79:109].strip(),
            "valor_bruto": line[109:120],
            "valor_desconto": line[120:131],
            "valor_liquido": line[131:142],
        }

    def parse_cc(self, line):
        return {
            "tipo": "CC",
            "codigo_estabelecimento": line[2:17],
            "nsu_transacao_original": line[17:29],
            "data_transacao_original": line[29:37],
            "numero_parcela": line[37:39],
            "nsu_cancelamento": line[39:51],
            "data_cancelamento": line[51:59],
        }

    def parse_l9(self, line):
        return {
            "tipo": "L9",
            "total_registros": line[2:8],
            "total_valores_creditos": line[8:22],
            "nseq": line[22:28],
        }

    def parse_a9(self, line):
        return {
            "tipo": "A9",
            "total_geral_registros": line[2:8],
            "nseq": line[8:14],
        }

    def get_records(self):
        return self.records
