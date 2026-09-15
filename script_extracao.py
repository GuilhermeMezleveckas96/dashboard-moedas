from datetime import datetime
import pandas as pd
import requests
import sys

try:
    # 1. Configurações da API do Banco Central (BCB)
    data_inicio = "01-01-2024"
    data_fim = datetime.now().strftime("%m-%d-%Y") 

    moedas = {
        "USD": "Dólar",
        "EUR": "Euro",
        "AUD": "Dólar Australiano",
        "GBP": "Libra",
        "SGD": "Dólar de Singapura",
    }

    # Cabeçalho de segurança para evitar bloqueio do servidor do GitHub (User-Agent)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    df_final = pd.DataFrame()

    print(f"Iniciando extração diária. Período: {data_inicio} até {data_fim}")

    for codigo, nome in moedas.items():
        url = (
            f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
            f"CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?"
            f"@moeda='{codigo}'&@dataInicial='{data_inicio}'&@dataFinalCotacao='{data_fim}'"
            f"&$top=10000&$format=json"
        )

        print(f"Buscando dados para {nome} ({codigo})...")
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 200:
            dados = response.json().get("value", [])
            if dados:
                df_moeda = pd.DataFrame(dados)
                df_moeda = df_moeda[["cotacaoCompra", "cotacaoVenda", "dataHoraCotacao"]].copy()
                df_moeda["Moeda_Codigo"] = codigo
                df_moeda["Moeda_Nome"] = nome
                df_final = pd.concat([df_final, df_moeda], ignore_index=True)
                print(f"-> Sucesso: {len(dados)} registros encontrados.")
            else:
                print(f"⚠️ API respondeu com sucesso, mas sem dados para {nome}.")
        else:
            print(f"❌ Erro na API do BCB para {nome}: Status {response.status_code}")

    # 2. Transformação e Limpeza dos Dados
    if not df_final.empty:
        print("\nTratando e estruturando a tabela final...")
        df_final["dataHoraCotacao"] = pd.to_datetime(df_final["dataHoraCotacao"])
        df_final["Data_Consulta"] = df_final["dataHoraCotacao"].dt.date
        df_final["Hora_Consulta"] = df_final["dataHoraCotacao"].dt.strftime("%H:%M:%S")
        df_final["Ano_Mes"] = df_final["dataHoraCotacao"].dt.to_period("M").astype(str)

        df_final = df_final.rename(columns={"cotacaoCompra": "Preco_Compra", "cotacaoVenda": "Preco_Venda"})
        
        df_final = df_final[["Data_Consulta", "Hora_Consulta", "Ano_Mes", "Moeda_Codigo", "Moeda_Nome", "Preco_Compra", "Preco_Venda"]]
        df_final = df_final.sort_values(by="Data_Consulta", ascending=False)

        # 3. Carga e Gravação
        df_final.to_csv("historico_moedas.csv", index=False, encoding="utf-8-sig")
        print("\n✅ SUCESSO COMPLETO! O arquivo 'historico_moedas.csv' foi atualizado na nuvem.")
    else:
        print("\n🚨 ERRO CRÍTICO: Nenhum dado foi coletado de nenhuma moeda. O arquivo não será salvo.")
        sys.exit(1) # Força o erro de forma controlada indicando falha na extração

except Exception as erro_interno:
    print(f"\n🚨 OCORREU UM ERRO DURANTE A EXECUÇÃO DO SCRIPT:")
    print(str(erro_interno))
    sys.exit(1)
