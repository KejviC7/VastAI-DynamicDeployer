# VastAI-DynamicDeployer
A Dynamic Deploying System for Vast.AI GPU Instances

This deployment bot is used to deploy GPU instances from vast.ai at scale based on your parameters. 

A few features of this fully dynamic bot:
1. Keeps tracks of instance states
2. Checks if an instance is stuck and if so deletes them
3. Peforms dynamic bidding for as long as nextBid is within the LIMIT COST configured in the system
4. Prevents duplicate deployment when the Vast api doesn't update the Instance IDs on their end even when we are already creating an instance etc
5. It dumps a json file containing only the instances that are in 'running' state. Contains SSH addrs and Port for each instance. 
