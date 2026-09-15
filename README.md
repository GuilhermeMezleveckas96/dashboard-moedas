# 📈 Dashboard & Pipeline de Câmbio BCB (Banco Central do Brasil)

[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/GuilhermeMezleveckas96/dashboard-moedas/main.yml?label=GitHub%20Actions)](https://github.com/GuilhermeMezleveckas96/dashboard-moedas/actions)
![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live-FF4B4B?logo=streamlit&logoColor=white)](https://dashboard-moedas-knpghpvcpwq8das8j7nqsq.streamlit.app/)
[![BCB API](https://img.shields.io/badge/API-BCB-blue)](https://www.bcb.gov.br/)

> Uma solução de Engenharia e Análise de Dados com execução automatizada em ambiente cloud. O projeto contém um pipeline automatizado de extração (ETL) conectado à API oficial do Banco Central do Brasil e um dashboard web interativo publicado com previsões estatísticas integradas.

## 🌐 Acesse o Projeto Publicado
O dashboard está online e pode ser acessado publicamente através do link abaixo:
👉 **[Visualizar o Dashboard de Moedas em Produção](https://dashboard-moedas-knpghpvcpwq8das8j7nqsq.streamlit.app/)**

---

## 🏗️ Arquitetura do Projeto na Nuvem

O ecossistema funciona de forma totalmente serverless (sem depender de nenhuma máquina local) e é dividido em três pilares principais:

1. **Pipeline de Extração (`script_extracao.py`):** Script em Python que consome a API OData do Banco Central, coleta o histórico das moedas (**USD, EUR, AUD, GBP, SGD**) desde 2024, realiza a limpeza de dados, padroniza as colunas e exporta as informações com codificação correta (`utf-8-sig`).
2. **Orquestração e Automação (GitHub Actions):** Um workflow configurado via arquivo YAML (`main.yml`) que provisiona automaticamente um runner Linux **todos os dias às 19:00h (Horário de Brasília)**. Ele executa o script de extração, captura os novos dados do dia e commita a atualização diretamente no repositório.
3. **Dashboard Interativo (`app.py`):** Interface web desenvolvida em Streamlit que lê a base de dados atualizada diretamente do GitHub, renderiza gráficos de linhas interativos via **Plotly**, exibe métricas de variação e calcula uma linha de tendência (Regressão Linear via NumPy) para projetar o preço dos próximos 5 dias úteis.

---

## 🛠️ Tecnologias Utilizadas

* **[GitHub Actions](https://github.com):** Orquestração, agendamento de tarefas (Cron job) e execução do pipeline CI/CD.
* **[Streamlit Cloud](https://streamlit.io):** Hospedagem, deploy e publicação da aplicação servida ao usuário final.
* **[Requests](https://requests.readthedocs.io/):** Consumo seguro e manipulação de requisições HTTP na API REST/OData do Banco Central.
* **[Pandas](https://pandas.pydata.org/):** Limpeza, transformação, enriquecimento e manipulação de séries temporais.
* **[Plotly Express](https://plotly.com):** Construção de gráficos dinâmicos, interativos e responsivos.
* **[NumPy](https://numpy.org):** Execução de cálculos estatísticos de ajuste polinomial (`polyfit`) para as projeções de tendência.

---

## 🚀 Como Executar o Projeto Localmente

### 📋 Pré-requisitos
Certifique-se de ter o **Python 3.8 ou superior** instalado em sua máquina.

### 🔧 Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com
   cd dashboard-moedas
   ```

2. **Instale todas as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o Pipeline de Dados (ETL) manualmente:**
   Rode este comando para forçar a busca de dados na API e gerar o arquivo CSV local:
   ```bash
   python script_extracao.py
   ```

4. **Inicie o Dashboard local do Streamlit:**
   Com o arquivo `historico_moedas.csv` gerado na pasta, inicialize a interface gráfica:
   ```bash
   streamlit run app.py
   ```

💡 O navegador abrirá automaticamente o painel no endereço local `http://localhost:8501`.

---

## 📊 Estrutura dos Dados Gerados (Data Schema)

O arquivo `historico_moedas.csv` mantido pelo pipeline segue a seguinte estrutura de colunas:

| Coluna | Tipo | Descrição | Exemplo |
| :--- | :--- | :--- | :--- |
| `Data_Consulta` | Date | Data da cotação oficial obtida da API | `2026-09-15` |
| `Hora_Consulta` | Time | Horário exato formatado (HH:MM:SS) | `13:05:42` |
| `Ano_Mes` | String | Agrupamento de período temporal (Ano-Mês) | `2026-09` |
| `Moeda_Codigo`| String | Sigla internacional de identification (3 letras) | `USD` |
| `Moeda_Nome` | String | Nome amigável da moeda tratado com acentuação | `Dólar` |
| `Preco_Compra` | Float | Cotação oficial de compra da moeda em BRL | `5.1234` |
| `Preco_Venda` | Float | Cotação oficial de venda da moeda em BRL | `5.1240` |

---

## 📝 Nota de Engenharia e Isenção de Responsabilidade
O modelo de projeção para os próximos 5 dias úteis utiliza uma **Regressão Linear Simples baseada nos últimos 30 registros históricos**. Esta aplicação possui caráter estritamente **educacional e demonstrativo de portfólio técnico**, portanto **não deve ser utilizada em nenhuma hipótese como recomendação real de investimentos, trading ou hedge financeiro**.
