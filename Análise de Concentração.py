import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo Excel
df = pd.read_excel(r'G:\Meu Drive\UFPE\Cadeiras\TCC\Relatórios\tcc_estorno_titulo_compensados.xlsx')

# Agrupar por usuário e contar o número de estornos
estornos_por_usuario = df.groupby('Usuario').size().reset_index(name='TotalEstornos')

# Ordenar os usuários pelo número de estornos em ordem decrescente
estornos_por_usuario = estornos_por_usuario.sort_values(by='TotalEstornos', ascending=False)

# Selecionar os TOP 5 usuários com mais estornos
top_5_usuarios = estornos_por_usuario.head(5)

# Criar o gráfico de barras horizontais
plt.figure(figsize=(10, 6))
bars = plt.barh(top_5_usuarios['Usuario'], top_5_usuarios['TotalEstornos'], color='darkblue')

# Adicionar os valores dentro das barras
for bar, valor in zip(bars, top_5_usuarios['TotalEstornos']):
    plt.text(bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, 
             str(valor), ha='center', va='center', color='white', fontsize=12, fontweight='bold')

# Configurações do gráfico
plt.xlabel('Total de Estornos')
plt.ylabel('Usuário')
plt.title('TOP 5 Usuários com Maiores Estornos em 2024')
plt.gca().invert_yaxis()  # Inverter o eixo Y para o maior valor ficar no topo
plt.show()