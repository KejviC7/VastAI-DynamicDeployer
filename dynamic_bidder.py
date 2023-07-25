import vast
import argparse
import time
import config
import helper
import destroy_deployments

def change_bid(instance_id, new_bid):
    # Create the Namespace object
    args = argparse.Namespace(
        url=config.URL,
        raw=False,
        price=new_bid,
        id=instance_id,
        api_key=config.API_KEY,
        func=vast.change__bid
    )
    
    # Send the API request
    try:
        resp = args.func(args)
    except:
        print(f"Error changing the bid of Instance: {instance_id} to new bid: {new_bid}\n")
    
    return 
def update_map(map, id):
    keys_to_delete = [key for key, value in map.items() if value == id]

    for key in keys_to_delete:
        del map[key]
    
    return map

def dynamic_bid(instances_map, multi_id_instances):
    sleep = 60
    helper.print_boxed_text("DYNAMIC BID ADJUSTING (IF REQUIRED)")
    inst_to_del = []

    for inst_id in instances_map.keys():
        if instances_map[inst_id]['Status'] == 'exited':
            try:
                print(f"\nInstance {inst_id} has been outbid. Increasing Bid to {float(instances_map[inst_id]['NextBid'])} to take Priority again.")
                if float(instances_map[inst_id]['NextBid']) <= instances_map[inst_id]['GPU_Count'] * config.LIMIT_COST:
                    time.sleep(5)
                    change_bid(int(inst_id), float(instances_map[inst_id]['NextBid']))
                else:
                    print(f"Can't increase bid further for Instance: {inst_id} as it already exceeds the maximum of {config.LIMIT_COST} per GPU.\n")
            except:
                print(f"Error changing the bid of Instance: {inst_id} to next bid: {instances_map[inst_id]['NextBid']}\n")

        elif instances_map[inst_id]['Status'] in ['created', 'loading']:
            print('Checking the Timestamp to determine if Instance is Stuck in Creating/Loading.\n')
            timestamp = instances_map[inst_id]['Timestamp']
            state_duration = time.time() - timestamp
            status = instances_map[inst_id]['Status']
            print(f'Instance {inst_id} has been in state: {status} for {state_duration} seconds.')
            
            if state_duration > 120:
                print(f"Instance {inst_id} is most likely stuck. Terminating it.")
                try:
                    destroy_deployments.destroy_instance(inst_id)
                    inst_to_del.append(inst_id)
                except: 
                    print(f"Failed to destroy stuck instance {inst_id}. Will retry...!")
    
    if inst_to_del:
        print("Updating MAPS after deleting stuck instances.")
        for id in inst_to_del:
            del instances_map[id]
            update_map(multi_id_instances, id)

    helper.print_boxed_text(f"Sleeping for {sleep} seconds to give time for the Instances to Spin-Up/Update States.")
    time.sleep(sleep)

    return instances_map, multi_id_instances
#change_bid(6384029, 0.12)
