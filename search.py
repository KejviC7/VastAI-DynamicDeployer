import argparse
import vast
import pandas as pd
import config

def filter_df(df, cost, upload):
    df = df[(df['$/GPUh'] <= cost) & (df['Net_up'].astype(float) >= upload)]
    df = df.sort_values(by='$/GPUh', ascending=True).reset_index(drop=True)

    return df

def search_offers(n_gpus, gpu, cost, upload):
    # Create the Namespace object
    args = argparse.Namespace(
        url=config.URL,
        raw=False,
        api_key=config.API_KEY,
        func=vast.search__offers,
        type='interruptible',
        no_default=False,
        disable_bundling=False,
        storage=5.0,
        order='score-',
        query=[f'gpu_name={gpu}'] if n_gpus == 0 else [f'num_gpus={n_gpus} gpu_name={gpu}']
    )

    # Send the API request
    try:
        data = args.func(args)
    except:
        print("Error querying for potential instances to deploy. Trying again...\n")
    
    data = filter_df(data, cost, upload)
    #print(data)
    # Collect the Instance IDs
    ids = data['ID'].tolist()
    bids = data['$/hr'].tolist()
    
    return data, ids, bids
