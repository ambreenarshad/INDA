import xml.etree.ElementTree as ET
import json
import os
from collections import defaultdict

UPLOADS_DIR = os.path.expanduser("~/INDA/VisioGns3/uploads")
OUTPUT_JSON = os.path.expanduser("~/INDA/VisioGns3/Generated_files/Connections.json")


def get_latest_upload(uploads_dir):
    """Return the most recent file from the uploads directory."""
    files = [os.path.join(uploads_dir, f) for f in os.listdir(uploads_dir) if os.path.isfile(os.path.join(uploads_dir, f))]
    if not files:
        raise FileNotFoundError("No files found in uploads directory.")
    return max(files, key=os.path.getmtime)  # newest file


def parse_drawio_xml(xml_file):
    """Parse draw.io XML to extract devices and connections with unique names."""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    devices = {}
    name_counter = defaultdict(int)
    connections = []

    # 1. Extract devices (vertex=1)
    for cell in root.findall(".//mxCell[@vertex='1']"):
        cell_id = cell.get("id")
        style = cell.get("style", "")
        shape_type = "Unknown"
        if "shape=" in style:
            shape_type = style.split("shape=")[1].split(";")[0]
            if "." in shape_type:  # only keep the last part
                shape_type = shape_type.split(".")[-1]

        # Count duplicates
        name_counter[shape_type] += 1
        count = name_counter[shape_type]

        # First one → plain name, later ones → add suffix
        if count == 1:
            unique_name = shape_type
        else:
            unique_name = f"{shape_type}-{count}"

        devices[cell_id] = {"id": cell_id, "base_name": shape_type, "unique_name": unique_name}

    # 2. Extract connections (edge=1)
    for cell in root.findall(".//mxCell[@edge='1']"):
        source = cell.get("source")
        target = cell.get("target")
        if source and target:
            connections.append({"from": source, "to": target})

    return devices, connections


def process_connections(devices, connections):
    """Replace device IDs in connections with unique names and assign adapter numbers."""
    processed = []
    port_tracker = defaultdict(int)  # keeps track of the next port for each device

    for conn in connections:
        src_id = conn["from"]
        dst_id = conn["to"]

        src_name = devices.get(src_id, {}).get("unique_name", src_id)
        dst_name = devices.get(dst_id, {}).get("unique_name", dst_id)

        # Assign next available port per device
        src_port = port_tracker[src_id]
        port_tracker[src_id] += 1

        dst_port = port_tracker[dst_id]
        port_tracker[dst_id] += 1

        processed.append({
            "from": src_name,
            "to": dst_name,
            "from_adapter_number": src_port,
            "to_adapter_number": dst_port
        })

    return processed


def main():
    latest_file = get_latest_upload(UPLOADS_DIR)
    print(f"Using latest uploaded file: {latest_file}")

    devices, connections = parse_drawio_xml(latest_file)
    processed_connections = process_connections(devices, connections)

    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(processed_connections, f, indent=4)

    print(f"Connections extracted and saved to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
