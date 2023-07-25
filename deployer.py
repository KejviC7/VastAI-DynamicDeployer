import search
import vast
import argparse
import config
import time


def deploy_instance(id, bid):
    # Create the Namespace object
    args = argparse.Namespace(
        url=config.URL,
        raw=False,
        api_key=config.API_KEY,
        func=vast.create__instance,
        id=id,
        price=bid,
        disk=3.0,
        image=config.IMAGE,
        login=None,
        label=None,
        onstart=None,
        onstart_cmd=None,
        ssh=True,
        jupyter=False,
        direct=False,
        jupyter_dir=None,
        jupyter_lab=False,
        lang_utf8=False,
        python_utf8=False,
        extra=None,
        env=None,
        args=None,
        create_from=None,
        force=False
    )

    # Send the API request
    try:
        resp = args.func(args)
        return resp
    except:
        print(f"Error deploying Instance {id}...Will retry...\n")
    #print(f"Deployed Instance {id} at price {bid}. New Contract ID is: {resp}")

# Mass Deployer
def multi_deployer(multi_id_tracker, ids, bids):
    for idx, id in enumerate(ids):
        time.sleep(3)
        # Only deploy an instance if that ID wasn't initialized before. Note: Sometimes 
        if id not in multi_id_tracker:
            try: 
                resp = deploy_instance(id, bids[idx])
                multi_id_tracker[id] = resp
                print(f"Instance ID {id} has been deployed. New Contract ID: {resp}\n")
            except:
                print(f"Error Deploying...\n")
        else:
            print(f"Instance ID: {id} has already been created. Preventing duplication...\n")
    
    return multi_id_tracker
        #print(resp)


