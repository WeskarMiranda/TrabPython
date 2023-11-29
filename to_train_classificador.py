import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn import preprocessing
from pickle import dump
from pickle import load

from imblearn.over_sampling import SMOTE

dados = pd.read_csv('E:/Nova Biblioteca/NovaBiblioteca/GitHub/TrabPython/breast-cancer(1)(1).csv', sep=',')
print(dados.info())

# Substituir valores ausentes
age_mapping = {'30-34': 32, 'lt40': 35, 'premeno': 0, 'ge40': 40, '40-49': 45, '50-59': 55, '60-69': 65}
dados.replace({'age': age_mapping}, inplace=True)

tumor_mapping = {'0-4': 2, '5-9': 7, '10-14': 12, '15-19': 17, '20-24': 22, '25-29': 27, '30-34': 32, '35-39': 37, '40-44': 42, '45-49': 47, '50-54': 52, '55-59': 57}
dados.replace({'tumor-size': tumor_mapping}, inplace=True)
# Codificação One-Hot
data = pd.get_dummies(dados, columns=['menopause', 'node-caps', 'breast', 'breast-quad', 'irradiat'])

# Mapeamento de valores ordinais
ordinal_mapping = {'30-34': 32, 'lt40': 35, 'premeno': 0, 'ge40': 1}
data.replace({'age': ordinal_mapping, 'tumor-size': ordinal_mapping, 'inv-nodes': ordinal_mapping, 'deg-malig': ordinal_mapping}, inplace=True)

# Mapeamento da variável alvo
target_mapping = {'no-recurrence-events': 0, 'recurrence-events': 1}
data.replace({'Class': target_mapping}, inplace=True)

# Verifique o DataFrame resultante
print(data)
# dados_num = dados.drop(columns=['Class'])

# dados_cat = dados['Class']

# # dados_num['age'] = pd.to_numeric(dados_num['age'].str.split('-').str[0], errors='coerce')
# # dados_num = dados_num[~dados_num['age'].isin(['ge40'])]
# # dados_num = dados_num.dropna()
# dados_num['age'] = dados_num['age'].replace('ge40', 40)




# dados_cat_normalizado = pd.get_dummies(data=dados_cat,prefix_sep='_', prefix='Class')
# print(dados_cat_normalizado)



# normalizador = preprocessing.MinMaxScaler()
# modelo_normalizador = normalizador.fit(dados_num)
# dados_num_normalizado = modelo_normalizador.fit_transform(dados_num)


# dados_final = pd.DataFrame(data = dados_num_normalizado, columns = ['age','menopause','tumor-size','inv-nodes','node-caps','deg-malig','breast','breast-quad','irradiat'])

# dados_final = dados_final.join(dados_cat_normalizado, how = 'left')
# print(dados_final)

# dump(modelo_normalizador,open('E:/Nova Biblioteca/NovaBiblioteca/GitHub/TrabPython/breast-cancer_normalizado.pkl', 'wb'))

# modelo_normalizador  = load(open('E:/Nova Biblioteca/NovaBiblioteca/GitHub/TrabPython/breast-cancer_normalizado.pkl', 'rb'))

# print(dados['Class'].value_counts())

# Segmentar os dados
dados_classes = dados['Class']
dados_atributos = dados.drop(columns = ['Class'])
# print(dados_atributos.columns)

# ---------------------------------------

tree = DecisionTreeClassifier() #Constrói o meta estimador para treinamento
atr_train, atr_test, class_train, class_test = train_test_split(dados_atributos, dados_classes, test_size =0.3 )
# print(class_test)

diagnosis_tree = tree.fit(atr_train, class_train)
Class_predict = diagnosis_tree.predict(atr_test)
# print(Class_predict)

print(dados)

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

print('# Frequencia das classes (atributo Output)')
print(dados.Class.value_counts())
dados.classes = dados['Class']
dados.atributos = dados.drop(columns=['Class'])

dados.atributos_normalizados = pd.get_dummies(dados.atributos)
print(dados.atributos.head())
print(dados.atributos_normalizados.head())

resampler = SMOTE()

dados.atributos_b, dados.classes_b = resampler.fit_resample(dados.atributos_normalizados, dados.classes)

from collections import Counter
class_count = Counter(dados.classes_b)
print(class_count)

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()

from sklearn.model_selection import cross_validate
scoringe=['precision_macro' , 'recall_macro']
scores_cross = cross_validate(rf, dados.atributos_b, dados.classes_b,cv=10, scoring= scoringe)
print('Matriz de sensibilidades:', scores_cross['test_precision_macro'])
print('Matriz de especificidades:', scores_cross['test_recall_macro'])

print('Especificidades:', scores_cross['test_recall_macro'].mean())
print('Sensibilidades:', scores_cross['test_precision_macro'].mean())

breast_cancer_rf = rf.fit(dados.atributos_b, dados.classes_b)
from pickle import dump
dump(breast_cancer_rf, open('E:/Nova Biblioteca/NovaBiblioteca/GitHub/TrabPython/breast-cancer_rf.pkl', 'wb'))