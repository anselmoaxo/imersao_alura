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
df_gpt = pd.read_excel('data/acao_pura.xlsx', sheet_name='Chatgpt')
df_gpt
#%%
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

df_principal = df_principal.merge(df_gpt, left_on='Nome_empresa',
                                  right_on='Nome da empresa' , how='left')
df_principal
# %%
df_principal = df_principal.drop(columns=['Nome da empresa'])
df_principal
# %%
df_principal = df_principal.rename(columns=
                                   {'Idade (anos)': 'idade'}).copy()
df_principal
# %%


df_principal['cat_idade'] = df_principal['idade'].apply(
    lambda x: 'mais que 100' if x > 100 else('menos de 50' if x < 50 else 'Entre 50 e 100')
)
df_principal
# %%
maior = df_principal['variacao_rs'].max()
menor = df_principal['variacao_rs'].min()
media = df_principal['variacao_rs'].mean()
condicao_subiu = df_principal['Resultado'] == 'Subiu'
condicao_desceu = df_principal['Resultado'] == 'Desceu'
media_subiu = df_principal[condicao_subiu]['variacao_rs'].mean()
media_desceu = df_principal[condicao_desceu]['variacao_rs'].mean()

dados = {
    'Maior': [maior],
    'Menor': [menor],
    'Media': [media],
    'Media_de_quem_Subiu': [media_subiu],
    'Media_de_quem_Desceu': [media_desceu]
}

# Criando o novo DataFrame
df_analise = pd.DataFrame(dados)
df_analise.to_excel('data/analise.xlsx', index=False)
# %%
df_principal_subiu = df_principal[condicao_subiu]
df_principal_subiu
# %%

df_analise_segmento = df_principal_subiu.groupby('Segmento')['variacao_rs'].sum().reset_index()
df_analise_segmento

# %%
df_analise_saldo = df_principal.groupby('Resultado')['variacao_rs'].sum().reset_index()
df_analise_saldo

# %%
import plotly.express as px
# %%
df_analise_saldo['variacao_rs_formatado'] = df_analise_saldo['variacao_rs'].apply(lambda x: '{:,.2f}'.format(x))

fig = px.bar(df_analise_saldo, x='Resultado', y='variacao_rs_formatado',
             text='variacao_rs_formatado', title='Variações R$ por Resultado',
             width=800, height=600)
fig.show()
# %%

fig = px.pie(df_analise_segmento, values='variacao_rs',
             names='Segmento', title='Gafico - Analise Segmento',
             width=800, height=600)
# %%
fig.show()
# %%
df_analise_cat_idade = df_principal.groupby('cat_idade')['variacao_rs'].sum().reset_index()
df_analise_cat_idade

fig = px.bar(df_analise_cat_idade, x='cat_idade', y='variacao_rs', text='variacao_rs', title='Variação Reais por Categoria de Idade',
             width=800, height=600)
fig.show()
# %%
