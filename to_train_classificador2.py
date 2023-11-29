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

# 1. Verificando a existencia de NaN
print(dados.head())
print(dados.isnull().sum())

# 2. Normalizacao dos dados
from sklearn.preprocessing import StandardScaler

normalizador = StandardScaler()

dados_num = dados.drop(columns=['Class'])

dados_normalizados = pd.DataFrame(data = normalizador.fit_transform(dados_num))

dados_normalizados.columns = dados_num.columns

# 3. Categorizacao dos dados
dados_cat = dados['Class']

dados_cat_normalizado = pd.get_dummies(data=dados_cat,prefix_sep='_', prefix='Class')

# 4. Union de dados categoricos e normalizados
dados_final = pd.DataFrame(data = dados_normalizados)

dados_final = dados_final.join(dados_cat_normalizado, how = 'left')

# 5. Salvando o normalizador
import pickle

pickle.dump(normalizador,open('E:/Nova Biblioteca/NovaBiblioteca/GitHub/TrabPython/breast-cancer_normalizado.pkl', 'wb'))



# 4. Modelo de arvore de decisão
from sklearn.tree import DecisionTreeClassifier

tree = DecisionTreeClassifier() #Constrói o meta estimador para treinamento

# 5. Separação de dados em treino e teste
from sklearn.model_selection import train_test_split

atr_train, atr_test, class_train, class_test = train_test_split(dados_final.drop(columns=['Class']), dados_final['Class'], test_size =0.3 )

# 6. Treinamento do modelo
diagnosis_tree = tree.fit(atr_train, class_train)

# 7. Predições
Class_predict = diagnosis_tree.predict(atr_test)

# 8. Matriz de confusão
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm=confusion_matrix(class_test, Class_predict)
disp = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels = tree.classes_)
disp.plot()
plt.show()

# 9. Cálculo da precisão
taxa_precisao =  tree.score(atr_test, class_test)
taxa_erros = 1 - taxa_precisao

print(f'Taxa de Precisão: {taxa_precisao:.2%}')
print(f'Taxa de Erros: {taxa_erros:.2%}')

# 10. Frequência das classes
print('# Frequencia das classes (atributo Output)')
print(dados.Class.value_counts())

# 11. Oversampling SMOTE
from imblearn.over_sampling import SMOTE

dados.atributos = dados_final.drop(columns=['Class'])
dados.classes = dados['Class']

resampler = SMOTE()

dados.atributos_b, dados.classes_b = resampler.fit_resample(dados.atributos, dados.classes)

from collections import Counter
class_count = Counter(dados.classes_b)
print(class_count)

# 12. Random Forest
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()

from sklearn.model_selection import cross_validate
scoringe=['precision_macro' , 'recall_macro']
scores_cross = cross_validate(rf, dados.atributos_b, dados.classes_b,cv=10, scoring= scoringe)
print('Matriz de sensibilidades:', scores_cross['test_precision_macro'])
print('Matriz de especificidades:', scores_cross['test_recall_macro'])

print('Especificidades:', scores_cross['test_recall_macro'].mean())
print('Sensibilidades:', scores_cross['test_precision_macro'].mean())

# 13. Salvando o modelo de Random Forest
breast_cancer_rf = rf.fit(dados.atributos_b, dados.classes_b)
from pickle import dump
pickle.dump(breast_cancer_rf, open('E:/Nova Biblioteca/NovaBiblioteca/GitHub/TrabPython/breast-cancer_rf.pkl', 'wb'))
