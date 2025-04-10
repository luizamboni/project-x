from .mcc_5812 import processar_mcc_5812
from .mcc_5814 import processar_mcc_5814
from .mcc_4121 import processar_mcc_4121
from .mcc_5411 import processar_mcc_5411
from .mcc_5813 import processar_mcc_5813

descricao_to_func = {
    "Restaurantes": processar_mcc_5812,
    "Fast Food": processar_mcc_5814,
    "Táxis e Limusines": processar_mcc_4121,
    "Supermercado": processar_mcc_5411,
    "Bar / Clube": processar_mcc_5813,
    "Bar / Clube / Casa Noturna": processar_mcc_5813,
}

def aplicar_regra_por_descricao(descricao_mcc: str, valor_autorizado: float, valor_final: float, taxas: dict) -> dict:
    func = descricao_to_func.get(descricao_mcc)
    if not func:
        return {
            "status": "falha",
            "mensagem": f"Nenhuma função registrada para a descrição MCC: '{descricao_mcc}'"
        }
    return func(valor_autorizado, valor_final, taxas)