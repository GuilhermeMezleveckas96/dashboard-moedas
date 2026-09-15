# 📈 Dashboard & Pipeline de Câmbio BCB (Banco Central do Brasil)

> Uma solução completa de Engenharia e Análise de Dados. O projeto contém um pipeline automatizado de extração (ETL) conectado à API oficial do Banco Central do Brasil e um dashboard web interativo publicado em produção com previsões estatísticas integradas.

## 🌐 Acesse o Projeto Publicado
O dashboard está online e pode ser acessado por qualquer pessoa através do link abaixo:
👉 **[Clique aqui para visualizar o Dashboard em Produção](https://dashboard-moedas-knpghpvcpwq8das8j7nqsq.streamlit.app/)]**

---

## 🏗️ Arquitetura do Projeto

O sistema é dividido em duas partes principais:

1. **Pipeline de Extração (`etl_bcb.py`):** Consome a API OData do Banco Central, coleta o histórico das moedas (**USD, EUR, AUD, GBP, SGD**) desde 2024, realiza a limpeza, remove milissegundos dos horários, padroniza as colunas e exporta tudo para o arquivo `historico_moedas.csv` com codificação correta (`utf-8-sig`).
2. **Dashboard Interativo (`app.py`):** Lê o arquivo de dados, renderiza gráficos de linhas interativos via **Plotly**, exibe métricas em tempo real e calcula uma linha de tendência (Regressão Linear via NumPy) para projetar o preço dos próximos 5 dias úteis.

---

## 🛠️ Tecnologias Utilizadas

O ecossistema foi construído puramente em Python com as seguintes bibliotecas:
* **[Streamlit Cloud](https://streamlit.io):** Hospedagem e publicação da aplicação na nuvem.
* **[Requests](https://readthedocs.io):** Consumo da API REST/OData do Banco Central.
* **[Pandas](https://pydata.org):** Limpeza, transformação e manipulação das tabelas temporais.
* **[Plotly Express](https://plotly.com):** Gráficos interativos e responsivos.
* **[NumPy](https://numpy.org):** Cálculo de ajuste polinomial (`polyfit`) para as projeções matemáticas.

---

## 🚀 Como Executar o Projeto Localmente

### 📋 Pré-requisitos
Certifique-se de ter o **Python 3.8 ou superior** instalado em sua máquina.

### 🔧 Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com
   cd seu-repositorio
   ```

2. **Instale todas as dependências:**
   ```bash
   pip install requests streamlit pandas plotly numpy
   ```

3. **Execute o Pipeline de Dados (ETL):**
   Rode este comando para buscar os dados do Banco Central e gerar o arquivo CSV local:
   ```bash
   python etl_bcb.py
   ```

4. **Inicie o Dashboard local do Streamlit:**
   Com o arquivo `historico_moedas.csv` gerado na pasta, inicialize a interface gráfica:
   ```bash
   streamlit run app.py
   ```

💡 O navegador abrirá automaticamente o painel no endereço local `http://localhost:8501`.

---

## 📊 Estrutura dos Dados Gerados

O arquivo `historico_moedas.csv` gerado pelo pipeline segue rigorosamente a estrutura abaixo:

| Coluna | Descrição | Exemplo |
| :--- | :--- | :--- |
| `Data_Consulta` | Data da cotação oficial | `2026-09-15` |
| `Hora_Consulta` | Horário exato formatado (HH:MM:SS) | `13:05:42` |
| `Ano_Mes` | Agrupamento de período (Ano-Mês) | `2026-09` |
| `Moeda_Codigo`| Sigla internacional de 3 letras | `USD` |
| `Moeda_Nome` | Nome amigável da moeda (com acentos) | `Dólar` |
| `Preco_Compra` | Cotação oficial de compra em BRL | `5.1234` |
| `Preco_Venda` | Cotação oficial de venda em BRL | `5.1240` |

---

## 📝 Nota de Engenharia e Isenção de Responsabilidade
O modelo de projeção para os próximos 5 dias úteis utiliza uma **Regressão Linear Simples baseada nos últimos 30 registros históricos**. Esta aplicação possui caráter estritamente **educacional e demonstrativo de portfólio técnico**, portanto **não deve ser utilizada em nenhuma hipótese como recomendação real de investimentos ou trading**.
