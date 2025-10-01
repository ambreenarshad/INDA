import json
import os

# Base directory (root of your project)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  

# Paths (adjusted to your folder structure)
GENERATED_DIR = os.path.join(BASE_DIR, "Generated_files")
GNS3_SERVER_DETAILS = os.path.join(GENERATED_DIR, "gns3_server_details.txt")
VSDX_PATH_FILE = os.path.join(BASE_DIR, "vsdx_path.txt")
CONNECTIONS_FILE = os.path.join(GENERATED_DIR, "Connections.json")
OUTPUT_PLAYBOOK = os.path.join(BASE_DIR, "Main_playbooks", "Gns3_Connections.yaml")


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


def read_vsdx_path():
    """Read the saved VSDX file path from the 'vsdx_path.txt' file."""
    try:
        with open(VSDX_PATH_FILE, "r") as file:
            vsdx_file_path = file.read().strip()
        return vsdx_file_path
    except Exception as e:
        raise RuntimeError(f"Failed to read vsdx path: {e}")


def get_project_name_from_vsdx(vsdx_path):
    """Extract the project name from the VSDX file name without the extension."""
    return os.path.splitext(os.path.basename(vsdx_path))[0]


def generate_ansible_playbook(ip, port, connections_file, project_name):
    # Load the JSON data
    with open(connections_file, 'r') as file:
        connections = json.load(file)
    
    # Start creating the playbook content
    playbook = f"""---
- name: Create links in GNS3 project based on JSON file
  hosts: localhost
  gather_facts: no
  vars:
    gns3_server: "http://{ip}:{port}"
    project_name: "{project_name}"
    
  tasks:
    - name: Get all projects from GNS3
      uri:
        url: "{{{{ gns3_server }}}}/v2/projects"
        method: GET
        return_content: yes
      register: gns3_projects

    - name: Set project ID based on project name
      set_fact:
        project_id: "{{{{ (gns3_projects.json | selectattr('name', 'equalto', project_name) | list)[0].project_id }}}}"
      when: gns3_projects.json | selectattr('name', 'equalto', project_name) | list | length > 0
      
    - name: Check if the project is opened
      uri:
        url: "{{{{ gns3_server }}}}/v2/projects/{{{{ project_id }}}}"
        method: GET
        return_content: yes
      register: project_status

    - name: Open the project if it is not already opened
      uri:
        url: "{{{{ gns3_server }}}}/v2/projects/{{{{ project_id }}}}/open"
        method: POST
        return_content: yes
        status_code: [200, 201]
      when: project_status.json.status != "opened"
      
    - name: Retrieve device node IDs from the GNS3 project
      uri:
        url: "{{{{ gns3_server }}}}/v2/projects/{{{{ project_id }}}}/nodes"
        method: GET
        return_content: yes
      register: gns3_nodes
    """

    # Add the tasks for creating the links
    for connection in connections:
        from_device = connection['from']
        to_device = connection['to']
        from_adapter_number = connection['from_adapter_number']
        to_adapter_number = connection['to_adapter_number']
        
        playbook += f"""
    - name: Create link from {from_device} to {to_device}
      vars:
        device_map: "{{{{ gns3_nodes.json | items2dict(key_name='name', value_name='node_id') }}}}"
      uri:
        url: "{{{{ gns3_server }}}}/v2/projects/{{{{ project_id }}}}/links"
        method: POST
        body_format: json
        headers:
          Content-Type: application/json
        status_code: [200, 201]
        body:
          nodes:
          - node_id: "{{{{ device_map['{from_device}'] | default('') }}}}"
            adapter_number: {from_adapter_number}
            port_number: 0
          - node_id: "{{{{ device_map['{to_device}'] | default('') }}}}"
            adapter_number: {to_adapter_number}
            port_number: 0
        """
    
    return playbook


if __name__ == "__main__":
    ip, port = read_gns3_server_details(GNS3_SERVER_DETAILS)
    print(f"Using GNS3 server: IP={ip}, Port={port}")
    
    vsdx_file_path = read_vsdx_path()
    project_name = get_project_name_from_vsdx(vsdx_file_path)

    ansible_playbook = generate_ansible_playbook(ip, port, CONNECTIONS_FILE, project_name)

    # Write the playbook to a YAML file
    with open(OUTPUT_PLAYBOOK, 'w') as file:
        file.write(ansible_playbook)

    print(f"Ansible playbook generated successfully: {OUTPUT_PLAYBOOK}")
