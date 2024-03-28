#%%
import pandas as pd  # Importa a biblioteca pandas para manipulação de dados
import matplotlib.pyplot as plt  # Importa a biblioteca matplotlib para visualização de dados
import mplfinance as mpf  # Importa a biblioteca mplfinance para visualização de dados financeiros
import yfinance as yf  # Importa a biblioteca yfinance para baixar dados financeiros

# Baixa os dados de mercado para o ticker 'PETR4.SA' (Petrobras na bolsa de valores brasileira)
# para o período de 1º de janeiro de 2023 a 31 de dezembro de 2023.
dados = yf.download('PETR4.SA', start='2023-01-01', end='2023-12-31')

# Converte os dados baixados em um DataFrame do pandas para facilitar a manipulação e análise.
dados = pd.DataFrame(dados)

# Visualiza os primeiros 30 registros dos dados em um gráfico de candlestick com volume, 
# médias móveis de 14 e 7 períodos, usando o estilo 'sas'.
mpf.plot(dados.head(30), type='candle', figsize=(16, 8), volume=True, mav=(14, 7), style='sas')
# %%
