
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn import preprocessing
from pickle import dump
from pickle import load
#1. Avaliar a frequencia das classes
dados = pd.read_csv('C:/Users/Weskar/Documents/GitHub/TrabPython/wdbc.txt', sep = ',')
dados_num = dados.drop(columns=['Diagnosis'])
dados_cat = dados['Diagnosis']

dados_cat_normalizado = pd.get_dummies(data=dados_cat,prefix_sep='_', prefix='Diagnosis')
dados_cat_normalizado

normalizador = preprocessing.MinMaxScaler()
modelo_normalizador = normalizador.fit(dados_num) 
dados_num_normalizado = modelo_normalizador.fit_transform(dados_num)

dados_final = pd.DataFrame(data = dados_num_normalizado, columns = ['ID','radius1','texture1','perimeter1','area1','smoothness1','compactness1','concavity1','concave_points1','symmetry1','fractal_dimension1','radius2','texture2','perimeter2','area2','smoothness2','compactness2','concavity2','concave_points2','symmetry2','fractal_dimension2','radius3','texture3','perimeter3','area3','smoothness3','compactness3','concavity3','concave_points3','symmetry3','fractal_dimension3'])

dados_final = dados_final.join(dados_cat_normalizado, how = 'left')
dados_final

dump(modelo_normalizador,open('C:/Users/Weskar/Documents/GitHub/TrabPython/wdbc_normalizado.pkl', 'wb'))

modelo_normalizador  = load(open('C:/Users/Weskar/Documents/GitHub/TrabPython/wdbc_normalizado.pkl', 'rb'))

# print(dados['Diagnosis'].value_counts())

# Segmentar os dados
dados_classes = dados['Diagnosis']
dados_atributos = dados.drop(columns = ['Diagnosis'])
# print(dados_atributos.columns)

# ---------------------------------------

tree = DecisionTreeClassifier() #Constrói o meta estimador para treinamento
atr_train, atr_test, class_train, class_test = train_test_split(dados_atributos, dados_classes, test_size =0.3 )
# print(class_test)

diagnosis_tree = tree.fit(atr_train, class_train)
Class_predict = diagnosis_tree.predict(atr_test)
# print(Class_predict)

# ---------------------------------------

#MATRIZ DE CONTINGÊNCIA

cm=confusion_matrix(class_test, Class_predict)
disp = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels = tree.classes_)
disp.plot()
plt.show()

# ---------------------------------------

#CÁLCULO DE PRECISÃO

taxa_precisao =  tree.score(atr_test, class_test)
taxa_erros = 1 - taxa_precisao

print(f'Taxa de Precisão: {taxa_precisao:.2%}')
print(f'Taxa de Erros: {taxa_erros:.2%}')

