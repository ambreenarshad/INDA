import xml.etree.ElementTree as ET
import os
from collections import defaultdict

# Function to get the latest .svg file and list of older files
def get_latest_svg_file():
    uploads_dir = os.path.expanduser("~/INDA/VisioGns3/uploads")
    
    # Ensure the uploads folder exists
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    
    # Get all .svg files in the uploads directory
    svg_files = [f for f in os.listdir(uploads_dir) if f.endswith(".svg")]
    
    if not svg_files:
        print("No .svg files found in uploads folder.")
        return None, []
    
    # Sort by modification time (newest first)
    svg_files.sort(key=lambda f: os.path.getmtime(os.path.join(uploads_dir, f)), reverse=True)
    
    latest_svg = os.path.join(uploads_dir, svg_files[0])
    older_files = [os.path.join(uploads_dir, f) for f in svg_files[1:]]
    
    return latest_svg, older_files

# Delete old .svg files
def clean_old_svg_files(older_files):
    for file in older_files:
        try:
            os.remove(file)
            print(f"Deleted old SVG file: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")

# Save the path of the latest SVG
def save_svg_path(svg_file):
    path = os.path.expanduser("~/INDA/VisioGns3/vsdx_path.txt")
    with open(path, "w") as file:
        file.write(svg_file)

# Extract machine names from SVG
def extract_machine_names(svg_file):
    # Parse SVG with namespace handling
    tree = ET.parse(svg_file)
    root = tree.getroot()
    
    # Define namespaces for SVG parsing
    namespaces = {
        'svg': 'http://www.w3.org/2000/svg',
        'xlink': 'http://www.w3.org/1999/xlink'
    }
    
    machine_names = []
    name_counter = defaultdict(int)
    
    # Look for the embedded mxfile content attribute
    content_attr = root.get('content', '')
    
    if content_attr:
        # The content attribute contains the diagram data
        # We need to parse this as XML
        try:
            # Parse the embedded XML structure
            import html
            decoded_content = html.unescape(content_attr)
            
            # Extract mxGraphModel from the content
            content_root = ET.fromstring(decoded_content)
            
            # Find all mxCell elements in the embedded structure
            for cell in content_root.findall(".//mxCell"):
                style = cell.get("style", "")
                value = cell.get("value", "").strip()
                
                # Check for all Cisco device types
                if any(keyword in style for keyword in [
                    "mxgraph.cisco.routers",
                    "mxgraph.cisco.switches",
                    "mxgraph.cisco.computers_and_peripherals",
                    "mxgraph.cisco.servers",
                    "mxgraph.cisco.storage",
                    "mxgraph.cisco.hubs_and_gateways"
                ]):
                    if value:  # Use visible label if available
                        base_name = value
                    else:
                        # Extract device type from style
                        base = style.split(";")[0]
                        base_name = base.split(".")[-1]
                    
                    # Count duplicates
                    name_counter[base_name] += 1
                    if name_counter[base_name] > 1:
                        machine_name = f"{base_name}-{name_counter[base_name]}"
                    else:
                        machine_name = base_name
                    
                    machine_names.append(machine_name)
        except Exception as e:
            print(f"Error parsing embedded content: {e}")
    
    # Also check for direct g elements with data attributes (alternative SVG structure)
    for g in root.findall(".//{http://www.w3.org/2000/svg}g"):
        data_cell = g.get('data-cell-id', '')
        if data_cell:
            # Look for associated metadata
            for metadata in g.findall(".//{http://www.w3.org/2000/svg}metadata"):
                # Process metadata if present
                pass
    
    return machine_names

def main():
    latest_svg, older_files = get_latest_svg_file()
    
    if not latest_svg:
        print("No SVG file available for processing.")
        return
    
    # Delete older SVG files
    clean_old_svg_files(older_files)
    
    # Save latest SVG path
    save_svg_path(latest_svg)
    
    # Extract machine names
    try:
        machines = extract_machine_names(latest_svg)
        
        if not machines:
            print("No machines found in the SVG.")
            return
        
        # Save output to Generated_files/machine_names.txt
        output_dir = os.path.expanduser("~/INDA/VisioGns3/Generated_files")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "machine_names.txt")
        
        with open(output_path, "w") as f:
            for name in machines:
                f.write(name + "\n")
        
        print(f"Machine names saved to: {output_path}")
        print(f"Total devices found: {len(machines)}")
        
    except Exception as e:
        print(f"Error processing SVG: {e}")

if __name__ == "__main__":
    main()
