import os, pandas, requests

WEBHOOK_URL = "https://discord.com/api/webhooks/hidden"

def is_consolidating(df, percentage=2):
    recent_candlesticks = df[-15:]
    
    max_close = recent_candlesticks['Close'].max()
    min_close = recent_candlesticks['Close'].min()
    # avg_vol = recent_candlesticks['Volume'].mean()
    
    threshold = 1 - (percentage / 100)
    if min_close > (max_close * threshold):
        #print('The max close was {} and the min close was {} and the average daily volume was {}'.format(max_close, min_close, avg_vol))
        return True
    
    return False
    
def is_breaking_out(df, percentage=2):
    last_close = df[-1:]['Close'].values[0]
    
    if is_consolidating(df[:-1], percentage=percentage):
        recent_closes = df[-16:-1]
        
        if last_close > recent_closes['Close'].max():
            return True, last_close
        
    return False, last_close
    

for filename in os.listdir('datasets/1d_datasets'):
    df = pandas.read_csv('datasets/1d_datasets/{}'.format(filename))
    
    if df.empty:
        continue
    
    if is_consolidating(df):
        print('{} is consolidating'.format(filename))
    
    result, last_close = is_breaking_out(df, 5)
        
    if result:
        message = f"{filename} is breaking out at {last_close}"
        print(message)

        payload = {
        "username" : "alertbot",
        "content" : message
        }

        requests.post(WEBHOOK_URL, json=payload)