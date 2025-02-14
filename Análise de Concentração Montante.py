import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo Excel
df = pd.read_excel(r'G:\Meu Drive\UFPE\Cadeiras\TCC\Relatórios\tcc_estorno_titulo_compensados.xlsx')

# Agrupar por usuário e somar o valor total dos estornos
estornos_por_usuario = df.groupby('Usuario')['Montante'].sum().reset_index(name='TotalEstornos')

# Calcular o total geral de estornos
total_estornos = estornos_por_usuario['TotalEstornos'].sum()

# Calcular a porcentagem de contribuição de cada usuário
estornos_por_usuario['Porcentagem'] = (estornos_por_usuario['TotalEstornos'] / total_estornos) * 100

# Ordenar os usuários pelo valor total de estornos em ordem decrescente
estornos_por_usuario = estornos_por_usuario.sort_values(by='TotalEstornos', ascending=False)

# Selecionar os TOP 5 usuários com maiores valores de estornos
top_5_usuarios = estornos_por_usuario.head(5)

# Criar o gráfico de barras horizontais
plt.figure(figsize=(10, 6))
bars = plt.barh(top_5_usuarios['Usuario'], top_5_usuarios['TotalEstornos'], color='darkblue')

# Adicionar os valores e porcentagens dentro das barras
for bar, valor, porcentagem in zip(bars, top_5_usuarios['TotalEstornos'], top_5_usuarios['Porcentagem']):
    plt.text(bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, 
             f'R$ {valor:.2f}\n({porcentagem:.2f}%)', 
             ha='center', va='center', color='white', fontsize=10, fontweight='bold')

# Configurações do gráfico
plt.xlabel('Total de Estornos (R$)')
plt.ylabel('Usuário')
plt.title('TOP 5 Usuários com Maiores Valores de Estornos em 2024 (Método de Montante)')
plt.gca().invert_yaxis()  # Inverter o eixo Y para o maior valor ficar no topo
plt.show()

# Exibir a tabela com os dados consolidados
print("Tabela de Concentração de Estornos:")
print(top_5_usuarios)