import json
import os
import re
import yaml
import math

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  

GNS3_SERVER_DETAILS = os.path.join(BASE_DIR, "Generated_files", "gns3_server_details.txt")
TEMPLATES_JSON = os.path.join(BASE_DIR, "Generated_files", "gns3_templates.json")
MACHINE_NAMES_TXT = os.path.join(BASE_DIR, "Generated_files", "machine_names.txt")
VSDX_FILE_PATH = os.path.join(BASE_DIR, "vsdx_path.txt")

OUTPUT_YAML = os.path.join(BASE_DIR, "Main_playbooks", "Gns3_Machines.yaml")

# Default coordinates for devices
X_START = 100
Y_START = 100
X_INCREMENT = 50
Y_INCREMENT = 50


def read_vsdx_path():
    """Read the saved VSDX file path from the 'vsdx_path' file."""
    with open(VSDX_FILE_PATH, "r") as file:
        vsdx_file_path = file.read().strip()
    return vsdx_file_path
def get_project_name_from_vsdx(vsdx_path):
    """Extract the project name from the VSDX file name without the extension."""
    return os.path.splitext(os.path.basename(vsdx_path))[0]

def read_gns3_server_details(file_path):
    """Reads the GNS3 server details (IP and port) from the text file."""
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            ip = lines[0].strip()
            port = lines[1].strip()
            return ip, port
    except Exception as e:
        raise RuntimeError(f"Failed to read GNS3 server details: {e}")

def load_templates(json_file):
    """Loads the templates from the JSON file."""
    try:
        with open(json_file, "r") as file:
            return json.load(file)
    except Exception as e:
        raise RuntimeError(f"Failed to load templates JSON: {e}")

def load_machine_names(txt_file):
    """Loads the machine names from the text file."""
    try:
        with open(txt_file, "r") as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        raise RuntimeError(f"Failed to load machine names: {e}")

def normalize_name(name):
    """
    Normalizes the device name by:
    - Removing specific substrings like 'ONFrontView'.
    - Removing trailing numbers.
    - Retaining meaningful parts of the name.
    - Removing special characters like '-', '_', and spaces.
    - Converting to lowercase.
    """
    # Remove specific substrings like 'ONFrontView' and trailing numbers
    name = re.sub(r"ONFrontView.*$", "", name)
    # Remove special characters and convert to lowercase
    name = re.sub(r"[^a-zA-Z0-9]", "", name).lower()
    return name

def find_template(machine_name, templates):
    """
    Finds the template for the given machine name by matching its normalized name.
    """

    normalized_machine_name = normalize_name(machine_name)
    print(f"Normalized Machine Name: {normalized_machine_name}")
    for template_name, template_data in templates.items():
        normalized_template_name = normalize_name(template_name)
        print(f"Comparing with Template: {normalized_template_name}")
        # Match if normalized names are similar
        if normalized_machine_name in normalized_template_name or normalized_template_name in normalized_machine_name:
            print(f"Match found: {template_name}")
            return template_data
    print(f"No match for: {machine_name}")
    return None

def nearest_square_number(count):
    """Finds the nearest square number to the given count."""
    sqrt = math.sqrt(count)
    lower = math.floor(sqrt) ** 2
    upper = math.ceil(sqrt) ** 2
    return lower if (count - lower) < (upper - count) else upper

def generate_yaml(ip, port, machine_names, templates, output_file, project_name):
    """Generates the YAML file for the Ansible playbook."""
    yaml_content = f"""
- hosts: localhost
  gather_facts: no
  vars:
    gns3_url: "http://{ip}:{port}"
    ansible_python_interpreter: /usr/bin/python3
  tasks:
    - name: Create a new GNS3 project
      uri:
        url: "{{{{ gns3_url }}}}/v2/projects"
        method: POST
        headers:
          Content-Type: "application/json"
        body: |
          {{
            "name": "{project_name}"
          }}
        body_format: json
        return_content: yes
        status_code: 201
      register: project_result

    - name: Debug project creation result
      debug:
        var: project_result
"""

    # Calculate the nearest square number and grid size
    count = len(machine_names)
    nearest_square = nearest_square_number(count)
    grid_size = int(math.sqrt(nearest_square))

    # Coordinates for device placement on the canvas
    x_coord = X_START
    y_coord = Y_START
    x_step = X_INCREMENT
    y_step = Y_INCREMENT
    counter = 0

    for machine_name in machine_names:
        template = find_template(machine_name, templates)
        if template:
            # Prepare device details dynamically
            body_details = ',\n            '.join(f'"{key}": {json.dumps(value)}' for key, value in template.items() if key not in ['name', 'x', 'y','properties'])

            # Handle properties indentation and ensure replicate_network_connection_state is boolean
            if "properties" in template:
                properties = template["properties"]
                properties_details = ",\n".join(f"              \"{key}\": {json.dumps(value)}" for key, value in properties.items())
                body_details += f""",
            "properties": {{
{properties_details}
            }}"""

            yaml_content += f"""
    - name: Add {machine_name} to the project
      uri:
        url: "{{{{ gns3_url }}}}/v2/projects/{{{{ project_result.json.project_id }}}}/nodes"
        method: POST
        headers:
          Content-Type: "application/json"
        body: |
          {{
            "name": "{machine_name}",
            "x": {x_coord},
            "y": {y_coord},
            {body_details}
          }}
        body_format: json
        return_content: yes
        status_code: 201
      register: machine_result

    - name: Debug {machine_name} creation result
      debug:
        var: machine_result
"""
            # Update coordinates for next device
            x_coord += x_step
            counter += 1
            if counter % grid_size == 0:  # Move to the next row after grid_size devices
                x_coord = X_START
                y_coord += y_step
        else:
            print(f"Template for machine '{machine_name}' not found. Please install the required template.")

    # Write the generated YAML content to the output file
    try:
        with open(output_file, 'w') as file:
            file.write(yaml_content)
        print(f"YAML file has been generated: {output_file}")
    except Exception as e:
        raise RuntimeError(f"Failed to save YAML file: {e}")

def main():
   ip, port = read_gns3_server_details(GNS3_SERVER_DETAILS)
   
   vsdx_file_path = read_vsdx_path()
   project_name = get_project_name_from_vsdx(vsdx_file_path)
   
   templates = load_templates(TEMPLATES_JSON)
   
   machine_names = load_machine_names(MACHINE_NAMES_TXT)
   
   generate_yaml(ip, port, machine_names, templates, OUTPUT_YAML, project_name)

if __name__ == "__main__":
    main()