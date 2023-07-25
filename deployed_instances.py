import argparse
import vast
import pandas as pd
import config
import time

def instances(ssh_map=None):
    # Create the Namespace object
    args = argparse.Namespace(
        url=config.URL,
        raw=False,
        api_key=config.API_KEY,
        func=vast.show__instances
    )

    if ssh_map is None:
        ssh_map = {}

    # Send the API request
    try:
        resp = args.func(args)
    except:
        print("Error generating the State Map of Deployed Instances...\n")
        return ssh_map

    current_time = int(time.time())
    
    for index, row in resp.iterrows():
        ID = row['ID']
        status = row['Status']
        next_bid = row['$/hr']
        gpu_count = int(row['Num'].replace('x', ''))
        ssh_addr = row['SSH Addr']
        ssh_port = row['SSH Port']
        
        if ID in ssh_map:
            previous_status, previous_timestamp = ssh_map[ID]['Status'], ssh_map[ID]['Timestamp']
            
            if status != previous_status:
                # Update the timestamp for a new status
                ssh_map[ID]['Status'] = status
                ssh_map[ID]['Timestamp'] = current_time
        else:
            # Initialize the timestamp for a new ID
            ssh_map[ID] = {'Status': status, 'NextBid': next_bid, 'GPU_Count': gpu_count, 'SSH Addr': ssh_addr, 'SSH Port': ssh_port, 'Timestamp': current_time}

    return ssh_map
