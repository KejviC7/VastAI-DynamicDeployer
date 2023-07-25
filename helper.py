from tabulate import tabulate
import json

def dump_data(data):
    # Filter the dictionary to only include entries where 'Status' is 'running'
    running_data = {
        key: {'SSH Addr': value['SSH Addr'], 'SSH Port': value['SSH Port']} 
        for key, value in data.items() if value['Status'] == 'running'
    }

    # Write the filtered data to a JSON file
    with open('output.json', 'w') as f:
        json.dump(running_data, f)

def visualize(data):
    table = []
    headers = ['ID', 'Status', 'Next Bid', 'GPU Count', 'SSH Addr', 'SSH Port', 'Timestamp']

    for id, details in data.items():
        row = [id, details['Status'], details['NextBid'], details['GPU_Count'], details['SSH Addr'], details['SSH Port'], details['Timestamp']]
        table.append(row)

    table_str = tabulate(table, headers, tablefmt='fancy_grid')
    print(table_str)

def print_boxed_text(text):
    width = len(text) + 2  # Width of the box

    print(f"+{'-' * width}+")
    print(f"| {text} |")
    print(f"+{'-' * width}+")