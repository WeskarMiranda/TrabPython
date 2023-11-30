import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Ler os dados
dados = np.array([
    10.5, 11.2, 12, 13.5, 15.2, 14.8, 14.6, 15.3, 16, 17.2, 16.5, 18,
    10.8, 11.4, 12.2, 13.7, 15.6, 15, 14.9, 15.8, 16.3, 17.4, 16.8, 18.5,
    11.2, 12, 12.8, 14.2, 16, 15.4, 15.2, 16.1, 17, 17.8, 17.1, 19,
    11.5, 12.3, 13.2
])

dados_2024 = dados[0:12]
dados_2025 = dados[12:24]
dados_2026 = dados[24:36]
dados_2027 = dados[36:]

# dados_2024 = np.array([
#     10.5, 11.2, 12, 13.5, 15.2, 14.8, 14.6, 15.3, 16, 17.2, 16.5, 18
# ])

# dados_2025 = np.array([
#     10.8, 11.4, 12.2, 13.7, 15.6, 15, 14.9, 15.8, 16.3, 17.4, 16.8, 18.5
# ])

# dados_2026 = np.array([
#     11.2, 12, 12.8, 14.2, 16, 15.4, 15.2, 16.1, 17, 17.8, 17.1, 19
# ])

# dados_2027 = np.array([
#     11.5, 12.3, 13.2
# ])

# Calcular a média, a variancia, o desvio padrão e a mediana 
media = dados.mean()
desvio_padrao = dados.std()
mediana = np.median(dados)
mediana_2024 = np.median(dados_2024)
mediana_2025 = np.median(dados_2025)
mediana_2026 = np.median(dados_2026)
mediana_2027 = np.median(dados_2027)
tendencia = np.polyfit(x=np.array(range(len(dados))), y=dados, deg=1)[0].item()
variancia = 0
for i in range(len(dados)):
    variancia += (dados[i] - media)**2
variancia /= len(dados)

# Calcular Tendência e Previsão 2028/Previsões
previsao_2028 = media + tendencia
previsao_2029 = media + 2 * tendencia
previsao_2030 = media + 3 * tendencia
previsao_2031 = media + 4 * tendencia
previsao_2032 = media + 5 * tendencia


# Calcular Erro Medio e Erro Percentual
erro_medio = np.mean(previsao_2028 - dados)
erro_percentual_medio = np.mean((previsao_2028 - dados) / dados) * 100


# Calcular os quartis
min = dados.min()
q1 = np.percentile(dados, 25)
q2 = np.percentile(dados, 50)
q3 = np.percentile(dados, 75)
iqr = q3 - q1
max = dados.max()


# Imprimir os resultados
print(f"Média: {media}")
print(f"Tendência: {tendencia}")
print(f"Desvio padrão: {desvio_padrao}")
print(f"Variância: {variancia}")
print(f"Mediana: {mediana}")
print(f"Mediana de 2024: {mediana_2024}")
print(f"Mediana de 2025: {mediana_2025}")
print(f"Mediana de 2026: {mediana_2026}")
print(f"Mediana de 2027: {mediana_2027}")
print(f"Mínimo: {min}")
print(f"Maximo: {max}")
print(f"Q1: {q1}")
print(f"Q2: {q2}")
print(f"Q3: {q3}")
print(f"Intervalo interquantil: {iqr}")
print(f"Previsão para 2028: {previsao_2028}")
print(f"Previsão para 2029: {previsao_2029}")
print(f"Previsão para 2030: {previsao_2030}")
print(f"Previsão para 2031: {previsao_2031}")
print(f"Previsão para 2032: {previsao_2032}")
print(f"Erro médio: {erro_medio}")
print(f"Erro percentual médio: {erro_percentual_medio}")

# Plotar o gráfico de densidade
sns.kdeplot(dados)
plt.show()

# Plotar o gráfico boxplot
sns.boxplot(data=dados, palette="Set3", showfliers=True)
plt.title("Amplitudes da série de dados")
plt.show()

# Plotar o gráfico de controle
# 1. Criar uma nova série do tamanho da série de dados e que conterá o valor da média em todas as observações
vendas_media = np.zeros(len(dados))
vendas_media[:] = media

# 2. Criar uma nova série do tamanho da série de dados e que conterá a média mais 1x desvio padrão
vendas_limite_superior = np.zeros(len(dados))
vendas_limite_superior[:] = media + desvio_padrao

# 3. Criar uma nova série do tamanho da série de dados e que conterá a média menos 1x desvio padrão
vendas_limite_inferior = np.zeros(len(dados))
vendas_limite_inferior[:] = media - desvio_padrao

# Montar o gráfico
sns.lineplot(data=dados, label='Observações')
sns.lineplot(data=vendas_media, label='Média')
sns.lineplot(data=vendas_limite_superior, label='Limite superior')
sns.lineplot(data=vendas_limite_inferior, label='Limite inferior')
plt.title("Exemplo de gráfico de controle")
plt.legend()
plt.show()
