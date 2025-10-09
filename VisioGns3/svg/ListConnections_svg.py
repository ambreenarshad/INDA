import xml.etree.ElementTree as ET
import json
import os
import html
from collections import defaultdict

UPLOADS_DIR = os.path.expanduser("~/INDA/VisioGns3/uploads")
OUTPUT_JSON = os.path.expanduser("~/INDA/VisioGns3/Generated_files/Connections.json")

def get_latest_svg_upload(uploads_dir):
    """Return the most recent SVG file from the uploads directory."""
    files = [os.path.join(uploads_dir, f) for f in os.listdir(uploads_dir) 
             if os.path.isfile(os.path.join(uploads_dir, f)) and f.endswith('.svg')]
    if not files:
        raise FileNotFoundError("No SVG files found in uploads directory.")
    return max(files, key=os.path.getmtime)  # newest file

def parse_drawio_svg(svg_file):
    """Parse draw.io SVG to extract devices and connections with unique names."""
    # Parse SVG file
    tree = ET.parse(svg_file)
    root = tree.getroot()
    
    # Get the content attribute which contains the diagram data
    content_attr = root.get('content', '')
    
    if not content_attr:
        raise ValueError("No content attribute found in SVG file.")
    
    # Unescape HTML entities to get the XML structure
    decoded_content = html.unescape(content_attr)
    
    # Parse the embedded XML structure
    content_root = ET.fromstring(decoded_content)
    
    devices = {}
    name_counter = defaultdict(int)
    connections = []
    
    # 1. Extract devices (vertex=1)
    for cell in content_root.findall(".//mxCell[@vertex='1']"):
        cell_id = cell.get("id")
        style = cell.get("style", "")
        value = cell.get("value", "").strip()
        
        shape_type = "Unknown"
        
        # Try to get device name from value first
        if value:
            shape_type = value
        elif "shape=" in style:
            # Extract from style
            shape_parts = style.split("shape=")[1].split(";")[0]
            if "." in shape_parts:  # only keep the last part
                shape_type = shape_parts.split(".")[-1]
            else:
                shape_type = shape_parts
        
        # Count duplicates
        name_counter[shape_type] += 1
        count = name_counter[shape_type]
        
        # First one → plain name, later ones → add suffix
        if count == 1:
            unique_name = shape_type
        else:
            unique_name = f"{shape_type}-{count}"
        
        devices[cell_id] = {
            "id": cell_id, 
            "base_name": shape_type, 
            "unique_name": unique_name
        }
        
        print(f"Found device: ID={cell_id}, Name={unique_name}, Style={style[:60]}...")
    
    # 2. Extract connections (edge=1)
    for cell in content_root.findall(".//mxCell[@edge='1']"):
        source = cell.get("source")
        target = cell.get("target")
        
        if source and target:
            connections.append({"from": source, "to": target})
            print(f"Found connection: {source} → {target}")
    
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
    latest_file = get_latest_svg_upload(UPLOADS_DIR)
    print(f"Using latest uploaded SVG file: {latest_file}\n")
    
    devices, connections = parse_drawio_svg(latest_file)
    
    print(f"\nTotal devices found: {len(devices)}")
    print(f"Total connections found: {len(connections)}\n")
    
    processed_connections = process_connections(devices, connections)
    
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    
    with open(OUTPUT_JSON, "w") as f:
        json.dump(processed_connections, f, indent=4)
    
    print(f"Connections extracted and saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()