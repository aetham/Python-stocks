import pandas as pd
import yfinance as yf
import time
import plotly.express as px
from datetime import datetime
import statsmodels.api

delete_time = ['12:40:00', '12:50:00', '13:00:00', '13:10:00', '13:20:00', '13:40:00',
               '13:50:00', '14:00:00', '14:10:00', '14:20:00', '14:40:00', '14:50:00', '15:00:00', '15:10:00',
               '15:20:00', '15:40:00']
while True:
    # Download the data
    data = yf.download(tickers='AAPL', period='15d', interval='5m')
    df = pd.DataFrame(data)
    df = df.iloc[::2, :]
    df.to_csv('data.csv', date_format='%Y-%m-%d-%H:%M:%S')

    # Reading data from csv and modifying further
    first_read = pd.read_csv("data.csv")
    # Add times to different columns
    first_read['Time'] = pd.to_datetime(first_read['Datetime']).dt.time
    first_read.to_csv('data.csv')

    second_read = pd.read_csv("data.csv")
    # Deleting Times rows that are not needed and deleting previous indexing
    second_read = second_read[~second_read['Time'].isin(delete_time)]
    second_read.drop(second_read.columns[[0]], axis=1, inplace=True)

    # Getting x-axis data to the list
    datelist = pd.to_datetime(second_read['Datetime']).tolist()

    # Creating placeholders for the x-axis
    second_read['Datetime'] = pd.date_range(datetime.today(), periods=second_read.shape[0]).astype('int64')

    # Drawing the 2d figure
    figure = px.scatter(second_read, y="Close", x='Datetime', trendline="lowess", title="APPLE STOCK")

    # Updating x axis with values from the list
    figure.update_xaxes(
                        tickangle=77,
                        tickmode='array',
                        tickvals=second_read['Datetime'][0::1],
                        ticktext=[d.strftime('%Y-%m-%d-%H:%M') for d in datelist]
                        )


    figure.write_html("output.html")
    time.sleep(60)
    figure.show()
