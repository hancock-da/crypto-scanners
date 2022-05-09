import os, requests
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

WEBHOOK_URL = "https://discord.com/api/webhooks/hidden" #insert your Discord webhook here

datasets_path = "crypto-scanners/datasets/1d_datasets"

def get_optimum_clusters(df, saturation_point=0.01):
    '''
    With thanks to https://www.github.com/judopro for providing this function.
    :param df: dataframe
    :param saturation_point: The amount of difference we are willing to detect
    :return: clusters with optimum K centers
    This method uses elbow method to find the optimum number of K clusters
    We initialize different K-means with 1..10 centers and compare the inertias
    If the difference is no more than saturation_point, we choose that as K and move on
    '''

    wcss = []
    k_models = []

    size = min(11, len(df.index))
    for i in range(1, size):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(df)
        wcss.append(kmeans.inertia_)
        k_models.append(kmeans)

    # Compare differences in inertias until it's no more than saturation_point
    optimum_k = len(wcss)-1
    for i in range(0, len(wcss)-1):
        diff = abs(wcss[i+1] - wcss[i])
        if diff < saturation_point:
            optimum_k = i
            break

    #print("Optimum K is " + str(optimum_k + 1))
    optimum_clusters = k_models[optimum_k]

    return optimum_clusters


for filename in os.listdir(datasets_path):
    
    #if filename == 'ADXUSDT.csv':
    df = pd.read_csv(os.path.join(datasets_path, filename))
    
    if df.empty:
        continue
    
    lows = pd.DataFrame(data=df, index=df.index, columns=["Low"])
    highs = pd.DataFrame(data=df, index=df.index, columns=["High"])
    last_close = df.iloc[-1]["Close"]
    two_last_close = df.iloc[-2]["Close"]
    last_vol = df.iloc[-1]['Volume']


    low_clusters = get_optimum_clusters(lows)
    low_centers = low_clusters.cluster_centers_
    low_centers = np.sort(low_centers, axis=0)
    
    high_clusters = get_optimum_clusters(highs)
    high_centers = high_clusters.cluster_centers_
    high_centers = np.sort(high_centers, axis=0)
    
    # print(low_centers)
    # print(high_centers)
    
    for res in high_centers:
        result = False
        if res > two_last_close and res < last_close and last_vol > max(df.iloc[-11:-2]['Volume']):
            print('{} is breaking out closing at {} over resistance at {}'.format(filename, last_close, res))
            result = True
            
        if result:
            message = f"{filename} is breaking out at {last_close}"
            print(message)

            payload = {
            "username" : "alertbot",
            "content" : message
            }

            requests.post(WEBHOOK_URL, json=payload)