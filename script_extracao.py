from datetime import datetime
import pandas as pd
import requests

# 1. Configurações da API do Banco Central (BCB)
data_inicio = "01-01-2024"  # Mantém o histórico desde o início de 2024
data_fim = datetime.now().strftime("%m-%d-%Y") 

moedas = {
    "USD": "Dólar",
    "EUR": "Euro",
    "AUD": "Dólar Australiano",
    "GBP": "Libra",
    "SGD": "Dólar de Singapura",
}

df_final = pd.DataFrame()

print("Iniciando extração diária do Banco Central...")

for codigo, nome in moedas.items():
    # URL oficial do PTAX corrigida
    url = (
        f"https://bcb.gov.br"
        f"CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?"
        f"@moeda='{codigo}'&@dataInicial='{data_inicio}'&@dataFinalCotacao='{data_fim}'"
        f"&$top=10000&$format=json"
    )

    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json().get("value", [])
        if dados:
            df_moeda = pd.DataFrame(dados)
            df_moeda = df_moeda[["cotacaoCompra", "cotacaoVenda", "dataHoraCotacao"]].copy()
            df_moeda["Moeda_Codigo"] = codigo
            df_moeda["Moeda_Nome"] = nome
            df_final = pd.concat([df_final, df_moeda], ignore_index=True)

# 2. Transformação e Limpeza dos Dados
if not df_final.empty:
    print("Tratando novos dados...")
    df_final["dataHoraCotacao"] = pd.to_datetime(df_final["dataHoraCotacao"])
    df_final["Data_Consulta"] = df_final["dataHoraCotacao"].dt.date
    df_final["Hora_Consulta"] = df_final["dataHoraCotacao"].dt.strftime("%H:%M:%S")
    df_final["Ano_Mes"] = df_final["dataHoraCotacao"].dt.to_period("M").astype(str)

    df_final = df_final.rename(columns={"cotacaoCompra": "Preco_Compra", "cotacaoVenda": "Preco_Venda"})
    
    df_final = df_final[["Data_Consulta", "Hora_Consulta", "Ano_Mes", "Moeda_Codigo", "Moeda_Nome", "Preco_Compra", "Preco_Venda"]]
    df_final = df_final.sort_values(by="Data_Consulta", ascending=False)

    # 3. Salvando o arquivo com acentuação correta
    df_final.to_csv("historico_moedas.csv", index=False, encoding="utf-8-sig")
    print("✅ Base de dados 'historico_moedas.csv' atualizada com sucesso pelo robô!")
else:
    print("🚨 Falha na extração. O arquivo não foi modificado.")
