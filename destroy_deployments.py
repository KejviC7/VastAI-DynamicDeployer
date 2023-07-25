import argparse
import vast
import config

def destroy_instance(instance_id):
    # Create the Namespace object
    args = argparse.Namespace(
        url=config.URL,
        raw=False,
        id=instance_id,
        api_key=config.API_KEY,
        func=vast.destroy__instance
    )
    
    # Send the API request
    resp = args.func(args)

    return 

def destroy_all(instances_map):
    for inst_id in instances_map.keys():
        try: 
            destroy_instance(inst_id)
        except:
            print(f"There was an issue destroying instance: {inst_id}")


def destroy_non_running(instances_map):
    for inst_id in instances_map.keys():
        if instances_map[inst_id]['Status'] != 'running':
            try: 
                destroy_instance(inst_id)
            except:
                print(f"There was an issue destroying instance: {inst_id}")

