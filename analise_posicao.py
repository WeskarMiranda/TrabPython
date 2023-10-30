import seaborn as sns
import matplotlib.pyplot as plt

import random
import numpy as np

serie = [] #lista vazia
#série aleatória de 100 valores entre 7 e 500
serie = random.sample(range(7,500), 100)
#converter a list em ndarray (vetor de números)
serie = np.array(serie)
#Média, desvio padrão e mediana
print(type(serie))
print(serie.mean())
print(serie.std())
print(np.median(serie))

#Amplitude de classes com quartis
min = serie.min()
q1 = np.percentile(serie, 25)
q2 =np.percentile(serie, 50)
q3 =np.percentile(serie, 75)
max=serie.max()

print(min,q1,q2,q3,max)



#Gráfico de densidade
# sns.kdeplot(serie)
# plt.show()


# sns.boxplot(data = serie, palette="Set3",  showfliers=True)
# plt.title("Amplitudes da série de dados")
# plt.show()

#gráfico de controle
#1. Criar uma nova série do tamanho da série de dados e que conterá o valor da media em todas as observações
serie_media = np.zeros(len(serie))
serie_media[:] = serie.mean() #todas as obersavações ficam iguais  à média da série de dados

#2. Criar uma nova série do tamanho da série de dados e que conterá a média mais 1x desvio padrão
serie_limite_superior = np.zeros(len(serie))
serie_limite_superior[:] = serie.mean() + serie.std()

#3. Criar uma nova série do tamanho da série de dados e que conterá a média menos 1x desvio padrão
serie_limite_inferior = np.zeros(len(serie))
serie_limite_inferior[:] = serie.mean() - serie.std()

#Monta o gráfico
sns.lineplot(data=serie, label='Observações')
sns.lineplot(data=serie_media, label='Média')
sns.lineplot(data=serie_limite_superior, label='Limite superior')
sns.lineplot(data=serie_limite_inferior, label='Limite inferior')
plt.title("Exemplo de gráfico de controle")
plt.legend()
plt.show()
