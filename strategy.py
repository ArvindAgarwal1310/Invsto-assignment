import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import pandas_ta as ta
from sqlalchemy import create_engine

#MySQL database credentials
host = "localhost"
user = "root"
password = "9618233565"
database = "INVSTO"
table = "stock_data"

try:
    # BUilding engine/connection
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")


    #------------------------------------------------Momentum--------------------------------------
    # Read data from MySQL into a DataFrame using SQLAlchemy.
    query = f"SELECT datetime, close FROM {table} ORDER BY datetime ASC"
    df = pd.read_sql(query, engine, index_col='datetime', parse_dates=True)

    # Calculate the RSI (Relative Strength Index) using pandas_ta.
    df.ta.rsi(close='close', append=True)

    # Generating trading signals based on RSI levels.

    df['Signal'] = 0  # 0 represents no signal
    df.loc[df['RSI_14'] < 30, 'Signal'] = 1  # Buy signal when RSI is below 30
    df.loc[df['RSI_14'] > 70, 'Signal'] = -1  # Sell signal when RSI is above 70

    # Plotting the stock price and RSI.
    plt.figure(figsize=(12, 6))
    plt.plot(df['close'], label='Close Price')
    plt.plot(df['RSI_14'], label='RSI')

    # Plotting buy and sell signals.
    plt.plot(df[df['Signal'] == 1].index, df['close'][df['Signal'] == 1], '^', markersize=8, color='g', label='Buy Signal')
    plt.plot(df[df['Signal'] == -1].index, df['close'][df['Signal'] == -1], 'v', markersize=8, color='r', label='Sell Signal')

    plt.title('Stock Price and RSI for Momentum Trading')  #Detailing the Graph.
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()



    #--------------------------------------EMA----------------------------------------
    # Read data from MySQL into a DataFrame using SQLAlchemy.
    query = f"SELECT datetime, close , low ,high FROM {table} ORDER BY datetime ASC"
    df = pd.read_sql(query, engine, index_col='datetime', parse_dates=True)


    # tesing for EMA
    df['ema_12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['ema_21_low'] = df['low'].ewm(span=21, adjust=False).mean()
    df['ema_21_high'] = df['high'].ewm(span=21, adjust=False).mean()
    df['Signal'] = 0  # 0 represents no signal
    df.loc[((df['ema_12'] > df['ema_21_low'])), 'Signal'] = -1 #Bear


    df.loc[((df['ema_12'] > df['ema_21_low']) & (df['ema_12'] > df['ema_21_high'])), 'Signal'] = 0

    df.loc[((df['ema_12'] > df['ema_21_high'])), 'Signal'] = 1 #Bull


    # Plotting the stock price.
    plt.figure(figsize=(12, 6))
    plt.plot(df['close'], label='Close Price')

    # Plotting Bear and Bull signals.
    plt.plot(df[df['Signal'] == 1].index, df['close'][df['Signal'] == 1], '^', markersize=3, color='g',
             label='Bull')
    plt.plot(df[df['Signal'] == -1].index, df['close'][df['Signal'] == -1], 'v', markersize=3, color='r',
             label='Bear')

    plt.title('Stock Price and EMA Trading')  # Detailing the Graph.
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

except mysql.connector.Error as e:
    print(f"Error: {e}")
finally:
    # Close the SQLAlchemy engine
    if 'engine' in locals():
        engine.dispose()
        print("MySQL engine closed, Thank You")
