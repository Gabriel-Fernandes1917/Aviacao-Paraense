import pandas as pd
import duckdb

colunas = [
    "cnpj_basico",       
    "cnpj_ordem",         
    "cnpj_dv",            
    "matriz_filial",      
    "nome_fantasia",      
    "situacao_cadastral", 
    "data_situacao",      
    "motivo_situacao",    
    "nome_cidade_exterior", 
    "pais",
    "data_inicio_atividade",
    "cnae_principal", 
    "cnae_secundario",
    "tipo_logadouro",
    "logadouro",
    "numero",
    "complemento",
    "bairro", 
    "cep", 
    "uf",
    "municipio", 
    "ddd1",
    "telefone1",
    "ddd2", 
    "telefone2",
    "dd_do_fax",
    "fax",
    "email",
    "situacao_especial", 
    "data_situacao_especial" 
]

arquivos_csv = [
    'Estabelecimentos0/K3241.K03200Y0.D50510.ESTABELE',
    'Estabelecimentos1/K3241.K03200Y1.D50510.ESTABELE',
    'Estabelecimentos2/K3241.K03200Y2.D50510.ESTABELE',
    'Estabelecimentos3/K3241.K03200Y3.D50510.ESTABELE',
    'Estabelecimentos4/K3241.K03200Y4.D50510.ESTABELE'
]

dfs = []

for caminho in arquivos_csv:

    query = f"""
        SELECT 
            {', '.join([f'column{str(i).zfill(2)} AS {nome}' for i, nome in enumerate(colunas)])}
        FROM read_csv_auto(
            '../base/{caminho}',
            delim=';',
            all_varchar=True,
            ignore_errors=true
        )
        WHERE
            (
                cnae_principal LIKE '51111%' -- trans regular de passageiros
                OR
                cnae_principal LIKE '51129%' -- trans nao regular de passageiro
                OR
                cnae_principal LIKE '51200%' -- trans de carga
                OR
                cnae_principal LIKE '30415%' -- fabric de aeronaves
                OR
                cnae_principal LIKE '30423%' -- fabric de peças para aeronaves 
                OR
                cnae_principal LIKE '33163%' -- manutenção de aeronaves
                OR
                cnae_principal LIKE '8599602%' -- curso de pilotagem
            )
            AND
            (
                uf = 'PA'
            )
        """

    df_parcial = duckdb.sql(query).to_df()
    dfs.append(df_parcial)

df_final = pd.concat(dfs, ignore_index=True)

df_final.to_excel("../baseFiltered/estabelecimentos.xlsx", index=False)

