#ETL Microdados do INEP = Educação Superior
#Autor: Weskar
#Data: 12/09/2023

#Conectar na base do DW_INEP
import mysql.connector
import pandas as pd

#Dictionary com a config do banco para conexão
config = {
    'user':'root',
    'password':'wkr2003',
    'host': 'localhost',
    'database':'dw_inep',
    'port': '3306'
}
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # dados = pd.read_csv('C:/Users/Aluno/Downloads/Microdados do Censo da Educação Superior 2020/dados/MICRODADOS_CADASTRO_CURSOS_2020.CSV',sep=';', encoding='iso-8859-1')
    dados_2020 = pd.read_csv('E:/Downloads/Descarte/Microdados do Censo da Educação Superior 2020/dados/MICRODADOS_CADASTRO_CURSOS_2020.CSV'
                        ,sep=';'
                        , encoding='iso-8859-1'
                        , low_memory=False)
    dados_2020 = dados_2020.fillna('')    
    #UF
    dados_uf = pd.DataFrame(dados_2020['NO_UF'].unique(), columns = ['UF'])
    
    for i, r in dados_uf.iterrows(): 
        insert_statement = f"INSERT INTO dim_uf_2020 (tf_uf, uf) VALUES ({i + 1}, '{r['UF']}')"
        print(insert_statement)
        cursor.execute(insert_statement) 
        conn.commit()

    print("Uf 2020 deu Certo")
    
    #Municipio
    dados_municipio = pd.DataFrame(dados_2020['NO_MUNICIPIO'].unique(), columns=['MUNICIPIO'])

    for i, r in dados_municipio.iterrows(): 
        insert_statement = "INSERT INTO dim_municipio_2020 (tf_municipio, municipio) VALUES (%s, %s)"
        values = (i + 1, r['MUNICIPIO'])
        print(insert_statement, values)
        cursor.execute(insert_statement, values) 
        conn.commit()

    print("Municipio 2020 deu Certo")

    #modalidade ensino
    dados_modalidade = pd.DataFrame(dados_2020['TP_MODALIDADE_ENSINO'].unique(), columns = ['TP_MODALIDADE_ENSINO'])

    for i,r in dados_modalidade.iterrows():
        if r['TP_MODALIDADE_ENSINO'] == 1:
            insert_statement = f"INSERT INTO dim_modalidade_2020 (tf_modalidade, modalidade) VALUES({r['TP_MODALIDADE_ENSINO']}, 'Presencial')"
        elif  r['TP_MODALIDADE_ENSINO'] == 2:
            insert_statement = f"INSERT INTO dim_modalidade_2020 (tf_modalidade, modalidade) VALUES({r['TP_MODALIDADE_ENSINO']}, 'EAD')"

        print(insert_statement)
        cursor.execute(insert_statement)
        conn.commit()

    print("Modalidade 2020 deu Certo")

    # #CURSO
    dados_curso = pd.DataFrame(dados_2020['NO_CURSO'].unique(), columns = ['CURSO'])

    for i,r in dados_curso.iterrows():
        insert_statement = f"INSERT INTO dim_curso_2020 (tf_curso, curso) VALUES({i+1}, '{r['CURSO']}')"
        print(insert_statement)
        cursor.execute(insert_statement)
        conn.commit()
    
    print("Curso 2020 deu Certo")
    
    # #ano
    dados_ano= pd.DataFrame(dados_2020['NU_ANO_CENSO'].unique(), columns = ['ANO'])

    for i,r in dados_ano.iterrows():
        insert_statement = f"INSERT INTO dim_ano_2020 (tf_ano, ano) VALUES({i+1}, '{r['ANO']}')"
    
        cursor.execute(insert_statement)
        conn.commit()

    print("Ano 2020 deu Certo")
    
    # # #ies
    dados_IES_2020 = pd.read_csv('E:/Downloads/Descarte/Microdados do Censo da Educação Superior 2020/dados/MICRODADOS_CADASTRO_IES_2020.CSV'
                    ,sep=';'
                    , encoding='iso-8859-1'
                    , low_memory=False)
    dados_IES_2020 = dados_IES_2020[['CO_IES','NO_IES']]
    
    dados_IES_curso = pd.DataFrame(dados_2020['CO_IES'].unique(), columns = ['co_ies'])

    for i, r in dados_IES_curso.iterrows():
        #determinar o nome  da ies
        dados_IES_filtrado=dados_IES_2020[dados_IES_2020['CO_IES'] == r['co_ies']]
        no_ies = dados_IES_filtrado['NO_IES'].iloc[0].replace("'","")
        insert_statement = f"INSERT INTO dim_ies_2020 (tf_ies, ies) VALUES({i+1}, '{no_ies}')"
        print(insert_statement)
        cursor.execute(insert_statement)
        conn.commit()

    print("Ies 2020 deu Certo!")

    # #Fact matriculas
    for i, r in dados_2020.iterrows():
        if r['TP_MODALIDADE_ENSINO'] == 1:
            modalidade  = 'Presencial'
        elif  r['TP_MODALIDADE_ENSINO'] == 2:
            modalidade = 'EAD'

        if pd.isnull(r['NO_MUNICIPIO']):
            municipio = "NULL"
        else:
            municipio = r['NO_MUNICIPIO'].replace("'","")

        dados_IES_filtrado=dados_IES_2020[dados_IES_2020['CO_IES'] == r['CO_IES']]
        no_ies = dados_IES_filtrado['NO_IES'].iloc[0].replace("'","")


        insert_statement = f"""
        INSERT INTO fact_matriculas_2020 (matriculados,tf_ano,tf_curso,tf_ies,tf_uf,tf_municipio,tf_modalidade)
        SELECT DISTINCT * FROM
        (SELECT {r['QT_INSCRITO_TOTAL']}) as matriculados,
        (SELECT DISTINCT tf_ano FROM dim_ano_2020 WHERE ano = {r['NU_ANO_CENSO']}) as tf_ano,
        (SELECT DISTINCT tf_curso FROM dim_curso_2020 WHERE curso = '{r['NO_CURSO']}') as tf_curso,
        (SELECT DISTINCT tf_ies FROM dim_ies_2020 WHERE ies = '{no_ies}') as tf_ies,
        (SELECT DISTINCT tf_uf FROM dim_uf_2020 WHERE uf = '{r['NO_UF']}') as tf_uf,
        (SELECT DISTINCT tf_municipio FROM dim_municipio_2020 WHERE municipio = '{municipio}') as tf_municipio,
        (SELECT DISTINCT tf_modalidade FROM dim_modalidade_2020 WHERE modalidade = '{modalidade}') as tf_modalidade
        """
        print(insert_statement)
        cursor.execute(insert_statement)
        conn.commit()

    print('Acabou, mas continua no 2021...')


    dados_2021 = pd.read_csv('E:/Downloads/Descarte/Microdados do Censo da Educação Superior 2021/dados/MICRODADOS_CADASTRO_CURSOS_2021.CSV'
                        ,sep=';'
                        , encoding='iso-8859-1'
                        , low_memory=False)
    dados_2021 = dados_2021.fillna('')    
    #UF
    dados_uf = pd.DataFrame(dados_2021['NO_UF'].unique(), columns = ['UF'])
    
    for i, r in dados_uf.iterrows(): 
        insert_statement = f"INSERT INTO dim_uf_2021 (tf_uf, uf) VALUES ({i + 1}, '{r['UF']}')"
        print(insert_statement)
        cursor.execute(insert_statement) 
        conn.commit()

    print("Uf 2021 deu Certo")
    
    #Municipio
    dados_municipio = pd.DataFrame(dados_2021['NO_MUNICIPIO'].unique(), columns=['MUNICIPIO'])

    for i, r in dados_municipio.iterrows(): 
        insert_statement = "INSERT INTO dim_municipio_2021 (tf_municipio, municipio) VALUES (%s, %s)"
        values = (i + 1, r['MUNICIPIO'])
        print(insert_statement, values)
        cursor.execute(insert_statement, values) 
        conn.commit()

    print("Municipio 2021 deu Certo")

    #modalidade ensino
    dados_modalidade = pd.DataFrame(dados_2021['TP_MODALIDADE_ENSINO'].unique(), columns = ['TP_MODALIDADE_ENSINO'])

    for i,r in dados_modalidade.iterrows():
        if r['TP_MODALIDADE_ENSINO'] == 1:
            insert_statement = f"INSERT INTO dim_modalidade_2021 (tf_modalidade, modalidade) VALUES({r['TP_MODALIDADE_ENSINO']}, 'Presencial')"
        elif  r['TP_MODALIDADE_ENSINO'] == 2:
            insert_statement = f"INSERT INTO dim_modalidade_2021 (tf_modalidade, modalidade) VALUES({r['TP_MODALIDADE_ENSINO']}, 'EAD')"

        print(insert_statement)
        cursor.execute(insert_statement)
        conn.commit()

    print("Modalidade 2021 deu Certo")

    # #CURSO
    dados_curso = pd.DataFrame(dados_2021['NO_CURSO'].unique(), columns = ['CURSO'])

    for i,r in dados_curso.iterrows():
        insert_statement = f"INSERT INTO dim_curso_2021 (tf_curso, curso) VALUES({i+1}, '{r['CURSO']}')"
        print(insert_statement)
        cursor.execute(insert_statement)
        conn.commit()
    
    print("Curso 2021 deu Certo")
    
    # #ano
    dados_ano= pd.DataFrame(dados_2021['NU_ANO_CENSO'].unique(), columns = ['ANO'])

    for i,r in dados_ano.iterrows():
        insert_statement = f"INSERT INTO dim_ano_2021 (tf_ano, ano) VALUES({i+1}, '{r['ANO']}')"
    
        cursor.execute(insert_statement)
        conn.commit()

    print("Ano 2021 deu Certo")
    
    # # #ies
    dados_IES_2021 = pd.read_csv('E:/Downloads/Descarte/Microdados do Censo da Educação Superior 2021/dados/MICRODADOS_CADASTRO_IES_2021.CSV'
                    ,sep=';'
                    , encoding='iso-8859-1'
                    , low_memory=False)
    dados_IES_2021 = dados_IES_2021[['CO_IES','NO_IES']]
    
    dados_IES_curso = pd.DataFrame(dados_2021['CO_IES'].unique(), columns = ['co_ies'])

    for i, r in dados_IES_curso.iterrows():
        #determinar o nome  da ies
        dados_IES_filtrado=dados_IES_2021[dados_IES_2021['CO_IES'] == r['co_ies']]
        no_ies = dados_IES_filtrado['NO_IES'].iloc[0].replace("'","")
        insert_statement = f"INSERT INTO dim_ies_2021 (tf_ies, ies) VALUES({i+1}, '{no_ies}')"
        print(insert_statement)
        cursor.execute(insert_statement)
        conn.commit()

    print("Ies 2021 deu Certo!")

    # #Fact matriculas
    for i, r in dados_2021.iterrows():
        if r['TP_MODALIDADE_ENSINO'] == 1:
            modalidade  = 'Presencial'
        elif  r['TP_MODALIDADE_ENSINO'] == 2:
            modalidade = 'EAD'

        if pd.isnull(r['NO_MUNICIPIO']):
            municipio = "NULL"
        else:
            municipio = r['NO_MUNICIPIO'].replace("'","")

        dados_IES_filtrado=dados_IES_2021[dados_IES_2021['CO_IES'] == r['CO_IES']]
        no_ies = dados_IES_filtrado['NO_IES'].iloc[0].replace("'","")


        insert_statement = f"""
        INSERT INTO fact_matriculas_2021 (matriculados,tf_ano,tf_curso,tf_ies,tf_uf,tf_municipio,tf_modalidade)
        SELECT DISTINCT * FROM
        (SELECT {r['QT_INSCRITO_TOTAL']}) as matriculados,
        (SELECT DISTINCT tf_ano FROM dim_ano_2021 WHERE ano = {r['NU_ANO_CENSO']}) as tf_ano,
        (SELECT DISTINCT tf_curso FROM dim_curso_2021 WHERE curso = '{r['NO_CURSO']}') as tf_curso,
        (SELECT DISTINCT tf_ies FROM dim_ies_2021 WHERE ies = '{no_ies}') as tf_ies,
        (SELECT DISTINCT tf_uf FROM dim_uf_2021 WHERE uf = '{r['NO_UF']}') as tf_uf,
        (SELECT DISTINCT tf_municipio FROM dim_municipio_2021 WHERE municipio = '{municipio}') as tf_municipio,
        (SELECT DISTINCT tf_modalidade FROM dim_modalidade_2021 WHERE modalidade = '{modalidade}') as tf_modalidade
        """
        print(insert_statement)
        cursor.execute(insert_statement)
        conn.commit()

    print('Acabou!')



except Exception as e:
    print(e)