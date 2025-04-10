def processar_mcc_5812(valor_autorizado: float, valor_final: float, taxas: dict) -> dict:
    limite_maximo = valor_autorizado * 1.20

    if valor_final > limite_maximo:
        return {
            "status": "falha",
            "mensagem": "Valor excede os 20% permitidos para MCC 5812. Requer nova autorização.",
            "limite_maximo_permitido": round(limite_maximo, 2)
        }

    irf = valor_final * taxas.get('irf', 0)
    bandeira = valor_final * taxas.get('bandeira', 0)
    adquirente = valor_final * taxas.get('adquirente', 0)
    subadquirente = valor_final * taxas.get('subadquirente', 0)

    total_taxas = irf + bandeira + adquirente + subadquirente
    valor_liquido = valor_final - total_taxas

    return {
        "status": "sucesso",
        "mcc": "5812",
        "descricao": "Restaurantes",
        "valor_autorizado": round(valor_autorizado, 2),
        "valor_final": round(valor_final, 2),
        "limite_maximo_permitido": round(limite_maximo, 2),
        "divisão": {
            "emissor (IRF)": round(irf, 2),
            "bandeira (Visa)": round(bandeira, 2),
            "adquirente": round(adquirente, 2),
            "subadquirente": round(subadquirente, 2),
        },
        "valor_liquido_para_o_estabelecimento": round(valor_liquido, 2)
    }