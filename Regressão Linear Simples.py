import pyodbc
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Conectar ao SQL Server
def retornar_conexao_sql():
    server = 'yyyy'
    database = 'yyyy'
    username = 'xxxx'
    password = 'xxxx'
    driver = 'ODBC Driver 17 for SQL Server'
    string_conexao = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password};'
    conexao = pyodbc.connect(string_conexao)
    return conexao

# Estabelecer a conexão
conexao = retornar_conexao_sql()

# Definir a consulta SQL ajustada
query = """
WITH Pedidos AS (
  SELECT
    DATEPART(MONTH, NF.PSTDAT) AS Mes,
    COUNT(NF.NFENUM) AS Total_Pedidos
  FROM
    [SAPPS4300].[dbo].[J_1BNFDOC] AS NF
  WHERE
    NF.BUKRS = '2000' AND
    NF.DIRECT = '2' AND
    NF.NFTYPE = 'YC' AND
    NF.PSTDAT BETWEEN '20220501' AND '20240730' AND
    NF.NATOP LIKE '%Vnd.mer.adq%'
  GROUP BY
    DATEPART(MONTH, NF.PSTDAT)
),
Faturamento AS (
  SELECT
    DATEPART(MONTH, NF.PSTDAT) AS Mes,
    SUM(NF.NFTOT) AS Faturamento
  FROM
    [SAPPS4300].[dbo].[J_1BNFDOC] AS NF
  WHERE
    NF.BUKRS = '2000' AND
    NF.PARID > '10000000000' AND
    NF.DIRECT = '2' AND
    NF.NFTYPE = 'YC' AND
    NF.CANCEL <> 'X' AND
    NF.PSTDAT BETWEEN '20220501' AND '20240730' AND
    NF.NATOP LIKE '%Vnd.mer.adq%'
  GROUP BY
    DATEPART(MONTH, NF.PSTDAT)
)
SELECT
  p.Mes,
  p.Total_Pedidos,
  f.Faturamento
FROM
  Pedidos AS p
LEFT JOIN
  Faturamento AS f
ON
  p.Mes = f.Mes
ORDER BY
  p.Mes;
"""

# Executar a consulta e carregar os dados em um DataFrame do Pandas
df = pd.read_sql(query, conexao)

# Fechar a conexão
conexao.close()

# Verificar se o DataFrame não está vazio
if df.empty:
    print("A consulta não retornou dados.")
else:
    # Exibir as primeiras linhas do DataFrame para verificação
    print(df.head())

    # Preparar os dados para a regressão linear
    # Verificar e tratar valores ausentes
    df = df.dropna(subset=['Total_Pedidos', 'Faturamento'])

    # Variáveis independentes e dependentes
    X = df[['Total_Pedidos']]  # Variável independente
    Y = df['Faturamento']  # Variável dependente

    # Adicionar uma constante à variável independente para o intercepto
    X = sm.add_constant(X)

    # Criar o modelo de regressão linear
    model = sm.OLS(Y, X).fit()

    # Exibir o resumo do modelo
    print(model.summary())

    # Plotar o gráfico de regressão linear
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Total_Pedidos'], df['Faturamento'], color='blue', label='Dados Reais')
    plt.plot(df['Total_Pedidos'], model.predict(X), color='red', label='Linha de Regressão')
    plt.xlabel('Quantidade de Pedidos')
    plt.ylabel('Faturamento')
    plt.title('Regressão Linear: Faturamento vs Quantidade de Pedidos')
    plt.legend()
    plt.grid(True)
    plt.show()