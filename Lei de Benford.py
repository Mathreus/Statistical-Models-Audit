import pyodbc
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Conexão com o banco de dados SQL Server
conn_str = (
    "Driver={SQL Server};"
    "Server=SEU_SERVIDOR;"
    "Database=SEU_BANCO_DE_DADOS;"
    "UID=SEU_USUARIO;"
    "PWD=SUA_SENHA;"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Consultando os dados
query = "SELECT SUA_COLUNA FROM SUA_TABELA"
cursor.execute(query)

# Recuperando os dados
dados = [row[0] for row in cursor.fetchall()]

# Fechando a conexão
cursor.close()
conn.close()

# Função para extrair o primeiro dígito
def primeiro_digito(numero):
    return int(str(numero).lstrip('0')[0])

# Aplicando a Lei de Benford
primeiros_digitos = [primeiro_digito(abs(int(valor))) for valor in dados if valor > 0]
contador_digitos = Counter(primeiros_digitos)

# Calculando a distribuição esperada pela Lei de Benford
benford = [np.log10(1 + 1/d) for d in range(1, 10)]

# Normalizando as contagens
total = sum(contador_digitos.values())
contagens = [contador_digitos[d] / total for d in range(1, 10)]

# Plotando os resultados
plt.figure(figsize=(10, 6))
plt.bar(range(1, 10), contagens, width=0.4, label="Dados Observados", align="center")
plt.plot(range(1, 10), benford, 'r--', label="Lei de Benford")
plt.xlabel('Primeiro Dígito')
plt.ylabel('Frequência Relativa')
plt.title('Distribuição de Frequências dos Primeiros Dígitos')
plt.legend()
plt.show()