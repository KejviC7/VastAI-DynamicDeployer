# Top Deployer by Amadeus

import vast
import deployer
import deployed_instances
import destroy_deployments
import dynamic_bidder
import helper
import search
import pandas as pd
import time
import config

# Parameters

GPU_MODEL = config.GPU_MODEL
GPU_COUNT = config.GPU_COUNT
LIMIT_COST = config.LIMIT_COST
MIN_UPLOAD = config.MIN_UPLOAD

DEPLOYED_INSTANCES_STATE = {}
MULTI_ID_INSTANCES = {}

# Mass Deployer
def multi_deployer(ids, bids):
    for idx, id in enumerate(ids):
        time.sleep(3)
        resp = deployer.deploy_instance(id, bids[idx])
        print(resp)
        

if __name__ == "__main__":

    
    # Collect Instance IDs for the provided search parameters 
    ''' 
    search_offers(0, 'RTX_4090', 0.5, 100)
    arg1 -> GPU count requirement. 0 -> check all configurations
    arg2 -> GPU Model
    arg3 -> Cost. Will filter out offers with cost > $0.5h
    arg4 -> Upload. Will filter out offers with upload < 100 Mb/s
    '''
    # Debugging - Destroy All Existing Instances before Start. You can comment it out
    helper.print_boxed_text("DESTROYING EXISTING INSTANCES")
    destroy_deployments.destroy_all(deployed_instances.instances())

    while True:
        timer = 150
        helper.print_boxed_text("SEARCHING FOR PROFITABLE INSTANCES")
        search_result, deployment_ids, bids = search.search_offers(GPU_COUNT, GPU_MODEL, LIMIT_COST, MIN_UPLOAD)
        print(search_result)
        
        # Deploy all Profitable Instances
        if len(deployment_ids) == 0:
            helper.print_boxed_text("NO NEW INSTANCES FOUND. SEARCHING...")
        else:
            helper.print_boxed_text("DEPLOYING NEW INSTANCES")
            MULTI_ID_INSTANCES = deployer.multi_deployer(MULTI_ID_INSTANCES, deployment_ids, bids)
        
        helper.print_boxed_text("Vast Instance ID - Deployed Instance ID MAP")
        print(MULTI_ID_INSTANCES)
        helper.print_boxed_text(f"Waiting for {timer} seconds to allow for State Updates")
        time.sleep(timer)
        
        # Monitor All Deployments for Dynamic Bidding 
        helper.print_boxed_text("CHECKING DEPLOYED INSTANCES")
        DEPLOYED_INSTANCES_STATE = deployed_instances.instances(DEPLOYED_INSTANCES_STATE)
        helper.visualize(DEPLOYED_INSTANCES_STATE)
        DEPLOYED_INSTANCES_STATE, MULTI_ID_INSTANCES = dynamic_bidder.dynamic_bid(DEPLOYED_INSTANCES_STATE, MULTI_ID_INSTANCES) 

        # Dump Deployed Instance Data to json for SSH Deployment
        helper.dump_data(DEPLOYED_INSTANCES_STATE)
        