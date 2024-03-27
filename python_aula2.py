#%%
import pandas as pd 
#%%
pd.options.display.float_format ='{:.2f}'.format
df_principal = pd.read_excel('data/acao_pura.xlsx', sheet_name='Principal')
df_principal
# %%
df_total_acoes = pd.read_excel('data/acao_pura.xlsx', sheet_name='Total_de_acoes')
df_total_acoes
# %%
df_tickers = pd.read_excel('data/acao_pura.xlsx', sheet_name='Ticker')
df_tickers
# %%
df_principal = df_principal[['Ativo', 'Data', 'Último (R$)',
                              'Var. Dia (%)']].copy()
df_principal

# %%
df_principal = df_principal.rename(columns={
                                        'Último (R$)': 'valor_final',
                                        'Var. Dia (%)': 'var_dia_pct'}).copy()
df_principal
# %%
df_principal['var_pct'] = df_principal['var_dia_pct'] / 100
df_principal['valor_inicial'] = df_principal['valor_final'] / (
                                df_principal['var_pct'] + 1)
df_principal
# %%
df_principal = df_principal.merge(df_total_acoes, left_on='Ativo',
                                  right_on='Código' , how='left')
df_principal
# %%
df_principal = df_principal.drop(columns=['Código'])
# %%
df_principal
# %%
df_principal['variacao_rs'] = (df_principal['valor_final'] - 
                               df_principal['valor_inicial']) * df_principal['Qtde. Teórica']
df_principal
# %%
df_principal['Qtde. Teórica'] = df_principal['Qtde. Teórica'].astype(int)
df_principal
# %%
df_principal = df_principal.rename(columns=
                                   {'Qtde. Teórica': 'qtd_teorica'}).copy()
df_principal
# %%
df_principal['Resultado'] = df_principal['variacao_rs'].apply(
                                    lambda x: 'Subiu' if x > 0 else (
                                        'Desceu' if x < 0 else 'Estavel'))
df_principal

# %%
df_principal = df_principal.merge(df_tickers, left_on='Ativo',
                                  right_on='Ticker' , how='left')
df_principal
# %%
df_principal = df_principal.drop(columns=['Ticker'])
df_principal

# %%
df_principal = df_principal.rename(columns={
    'Nome': 'Nome_empresa'
}).copy()

df_principal
# %%
