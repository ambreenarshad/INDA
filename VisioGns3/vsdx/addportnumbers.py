import json
import os

# Function to process the JSON and add adapter numbers
def add_adapter_numbers_to_json(input_file, output_file):
    # Read the JSON data from the input file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Dictionary to track adapter numbers for each device
    adapter_count = {}

    # Iterate through each connection and update adapter numbers
    for connection in data:
        # Process 'from' device
        from_device = connection["from"]
        if from_device not in adapter_count:
            adapter_count[from_device] = 0
        connection["from_adapter_number"] = adapter_count[from_device]
        adapter_count[from_device] += 1

        # Process 'to' device
        to_device = connection["to"]
        if to_device not in adapter_count:
            adapter_count[to_device] = 0
        connection["to_adapter_number"] = adapter_count[to_device]
        adapter_count[to_device] += 1

    # Write the updated JSON data to the output file
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

# Example usage
input_file = os.path.expanduser("~/INDA/VisioGns3/Generated_files/Connections.json")   # Replace with your input JSON file path
output_file = os.path.expanduser("~/INDA/VisioGns3/Generated_files/Connections.json") # Replace with your desired output file path

add_adapter_numbers_to_json(input_file, output_file)
