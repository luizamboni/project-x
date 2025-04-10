from .mcc_5812 import processar_mcc_5812
from .mcc_5814 import processar_mcc_5814
from .mcc_4121 import processar_mcc_4121
from .mcc_5411 import processar_mcc_5411
from .mcc_5813 import processar_mcc_5813
from .edi_parser import EDIParser

descricao_to_func = {
    "5812": processar_mcc_5812,
    "5814": processar_mcc_5814,
    "4121": processar_mcc_4121,
    "5411": processar_mcc_5411,
    "5813": processar_mcc_5813,
}

def aplicar_regra_por_descricao(mcc: str, valor_autorizado: float, valor_final: float, taxas: dict) -> dict:
    func = descricao_to_func.get(mcc)
    if not func:
        return {
            "status": "falha",
            "mensagem": f"Nenhuma função registrada para a descrição MCC: '{mcc}'"
        }
    return func(valor_autorizado, valor_final, taxas)