import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Configuração da página do Streamlit
st.set_page_config(page_title="Dashboard de Câmbio BCB", page_icon="📈", layout="wide")

st.title("📈 Dashboard Interativo de Cotações de Moedas")
st.markdown("Dados extraídos diretamente da API Oficial do Banco Central do Brasil.")

# 1. CARREGAMENTO DOS DADOS
# Substitua pela URL do seu repositório no GitHub (deve ser o link do arquivo "Raw")
# Exemplo: https://githubusercontent.com
URL_CSV = "historico_moedas.csv" # Se rodar local, ele lê o arquivo na mesma pasta

@st.cache_data # Cache para o site carregar instantaneamente sem ler o CSV toda hora
def carregar_dados(url):
    df = pd.read_csv(url, encoding="utf-8-sig")
    df["Data_Consulta"] = pd.to_datetime(df["Data_Consulta"])
    return df

try:
    df = carregar_dados(URL_CSV)
except Exception as e:
    st.error(f"Erro ao carregar o arquivo de dados: {e}")
    st.stop()

# 2. BARRA LATERAL (Filtros)
st.sidebar.header("🔍 Filtros de Consulta")

# Filtro de Moeda
lista_moedas = df["Moeda_Nome"].unique()
moeda_selecionada = st.sidebar.selectbox("Selecione a Moeda:", lista_moedas)

# Filtro de Período (Ano/Mês)
lista_meses = sorted(df["Ano_Mes"].unique(), reverse=True)
lista_meses.insert(0, "Todo o Período")
periodo_selecionado = st.sidebar.selectbox("Selecione o Mês/Ano:", lista_meses)

# Filtrando o DataFrame com base nas escolhas
df_filtrado = df[df["Moeda_Nome"] == moeda_selecionada]

if periodo_selecionado != "Todo o Período":
    df_filtrado = df_filtrado[df_filtrado["Ano_Mes"] == periodo_selecionado]

# Ordenando por data para o gráfico ficar correto (cronológico)
df_filtrado = df_filtrado.sort_values("Data_Consulta")

# 3. CARDS DE RESUMO (Última Cotação Disponível)
ultima_cotacao = df[df["Moeda_Nome"] == moeda_selecionada].sort_values("Data_Consulta", ascending=False).iloc[0]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label=f"Último Preço de Compra ({ultima_cotacao['Moeda_Codigo']})", value=f"R$ {ultima_cotacao['Preco_Compra']:.4f}")
with col2:
    st.metric(label="Preço de Venda", value=f"R$ {ultima_cotacao['Preco_Venda']:.4f}")
with col3:
    st.metric(label="Última Atualização", value=str(ultima_cotacao['Data_Consulta'].date()))

st.markdown("---")

# 4. GRÁFICO DE EVOLUÇÃO HISTÓRICA
st.subheader(f"📊 Evolução Histórica - {moeda_selecionada}")

fig = px.line(
    df_filtrado, 
    x="Data_Consulta", 
    y=["Preco_Compra", "Preco_Venda"],
    labels={"value": "Valor em Real (BRL)", "Data_Consulta": "Data", "variable": "Tipo"},
    title=f"Variação do preço do {moeda_selecionada} no período selecionado"
)
fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig, use_container_width=True)

# 5. INTELIGÊNCIA / MODELO DE PREVISÃO (Regressão Linear Simples para os próximos 5 dias)
st.markdown("---")
st.subheader("🔮 Tendência e Previsão (Próximos 5 dias úteis)")

# Usando todos os dados históricos da moeda para treinar a tendência recente (últimos 30 registros)
df_recente = df[df["Moeda_Nome"] == moeda_selecionada].sort_values("Data_Consulta").tail(30)

# Criando um índice numérico representando os dias para fazer o cálculo matemático da linha de tendência
df_recente['Dias_Indice'] = np.arange(len(df_recente))

# Ajuste da reta (Y = a*X + b) usando NumPy para achar a inclinação (Regressão Linear)
X = df_recente['Dias_Indice']
Y = df_recente['Preco_Venda']
coeficientes = np.polyfit(X, Y, 1) # Retorna [inclinação, intercepto]

# Projeção para os próximos 5 dias úteis
ult_indice = X.max()
futuro_indices = np.arange(ult_indice + 1, ult_indice + 6)
previsoes_futuras = np.polyval(coeficientes, futuro_indices)

# Criando as datas futuras
ultima_data = df_recente['Data_Consulta'].max()
datas_futuras = pd.date_range(start=ultima_data + pd.Timedelta(days=1), periods=5, freq='B')

df_previsao = pd.DataFrame({
    'Data Projetada': datas_futuras.strftime('%d/%m/%Y'),
    'Preço Previsto (Venda)': [f"R$ {p:.4f}" for p in previsoes_futuras]
})

# Exibindo os resultados na tela
col_table, col_text = st.columns([1, 2])

with col_table:
    st.dataframe(df_previsao, hide_index=True)

with col_text:
    inclinacao = coeficientes[0]
    if inclinacao > 0:
        st.success(f"📈 **Tendência de Alta:** O modelo matemático baseado nos últimos 30 dias indica que o **{moeda_selecionada}** tende a subir ligeiramente nos próximos dias.")
    else:
        st.warning(f"📉 **Tendência de Baixa:** O modelo matemático baseado nos últimos 30 dias indica que o **{moeda_selecionada}** tende a cair ligeiramente nos próximos dias.")
    st.info("💡 *Nota de Engenharia de Dados:* Esta previsão utiliza um modelo estatístico linear simples baseado no histórico recente para fins educacionais de portfólio. Não deve ser usado como recomendação financeira.")
