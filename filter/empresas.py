import pandas as pd
import duckdb

df_cnpjs = pd.read_excel('../baseFiltered/estabelecimentos.xlsx')
cnpjs_unicos = df_cnpjs['cnpj_basico'].dropna().unique().tolist()

df_filtro = pd.DataFrame({'cnpj_basico': cnpjs_unicos})

duckdb.register('filtro_cnpjs', df_filtro)

arquivos_csv = [
    'Empresas0/K3241.K03200Y0.D50510.EMPRECSV',
    'Empresas1/K3241.K03200Y1.D50510.EMPRECSV',
    'Empresas2/K3241.K03200Y2.D50510.EMPRECSV',
    'Empresas3/K3241.K03200Y3.D50510.EMPRECSV',
    'Empresas4/K3241.K03200Y4.D50510.EMPRECSV',
    'Empresas5/K3241.K03200Y5.D50510.EMPRECSV',
    'Empresas6/K3241.K03200Y6.D50510.EMPRECSV',
    'Empresas7/K3241.K03200Y7.D50510.EMPRECSV',
    'Empresas8/K3241.K03200Y8.D50510.EMPRECSV',
    'Empresas9/K3241.K03200Y9.D50510.EMPRECSV'
]

dfs = []

for arquivo in arquivos_csv:
    query = f"""
        SELECT s.*
        FROM read_csv_auto('../base/{arquivo}', delim=';', all_varchar=True, ignore_errors=true) AS s
        INNER JOIN filtro_cnpjs f
        ON s.column0 = f.cnpj_basico
    """
    df_resultado = duckdb.sql(query).to_df()
    dfs.append(df_resultado)

df_final = pd.concat(dfs, ignore_index=True)

df_final.to_excel("../baseFiltered/empresas.xlsx", index=False)