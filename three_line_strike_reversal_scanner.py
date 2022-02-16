import talib
import os, requests
import pandas as pd

WEBHOOK_URL = "https://discord.com/api/webhooks/hidden"

for filename in os.listdir('datasets/1d_datasets'):
    with open('datasets/1d_datasets/{}'.format(filename)) as f:

        df = pd.read_csv(f)
        df['Date'] = pd.to_datetime(df['Date'], unit='ms')
        if df.empty:
            continue
        
        three_line_strike = talib.CDL3LINESTRIKE(df['Open'], df['High'], df['Low'], df['Close'])
        fastsma = talib.SMA(df['Close'], timeperiod=9)
        slowsma = talib.SMA(df['Close'], timeperiod=50)
        
        df['Three Line Strike'] = three_line_strike
        df['Fast SMA'] = fastsma
        df['Slow SMA'] = slowsma 
        
        #print(df)
        
        if any(df.iloc[-5:-1]['Three Line Strike'] == -100) and df.iloc[-1]['Fast SMA'] < df.iloc[-1]['Slow SMA']:
            
            message = "{} has a possible three line strike reversal in the last 5 days".format(filename)
            print(message)
            print(df.iloc[-5:-1])

            payload = {
            "username" : "alertbot",
            "content" : message
            }

            requests.post(WEBHOOK_URL, json=payload)
        #elif df.iloc[-1,:]['Three Line Strike'] == 0:
            #print('{} has no pattern'.format(filename))
      