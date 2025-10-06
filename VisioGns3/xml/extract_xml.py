import xml.etree.ElementTree as ET
import os
from collections import defaultdict

# Function to get the latest .xml file and list of older files
def get_latest_xml_file():
    uploads_dir = os.path.expanduser("~/INDA/VisioGns3/uploads")

    # Ensure the uploads folder exists
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

    # Get all .xml files in the uploads directory
    xml_files = [f for f in os.listdir(uploads_dir) if f.endswith(".xml")]

    if not xml_files:
        print("No .xml files found in uploads folder.")
        return None, []

    # Sort by modification time (newest first)
    xml_files.sort(key=lambda f: os.path.getmtime(os.path.join(uploads_dir, f)), reverse=True)

    latest_xml = os.path.join(uploads_dir, xml_files[0])
    older_files = [os.path.join(uploads_dir, f) for f in xml_files[1:]]

    return latest_xml, older_files

# Delete old .xml files
def clean_old_xml_files(older_files):
    for file in older_files:
        try:
            os.remove(file)
            print(f"Deleted old XML file: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")

# Save the path of the latest XML
def save_xml_path(xml_file):
    path = os.path.expanduser("~/INDA/VisioGns3/vsdx_path.txt")
    with open(path, "w") as file:
        file.write(xml_file)

# Extract machine names from XML
def extract_machine_names(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    machine_names = []
    name_counter = defaultdict(int)

    for cell in root.findall(".//mxCell"):
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

    return machine_names

def main():
    latest_xml, older_files = get_latest_xml_file()

    if not latest_xml:
        print("No XML file available for processing.")
        return

    # Delete older XML files
    clean_old_xml_files(older_files)

    # Save latest XML path
    save_xml_path(latest_xml)

    # Extract machine names
    try:
        machines = extract_machine_names(latest_xml)
        if not machines:
            print("No machines found in the XML.")
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
        print(f"Error processing XML: {e}")

if __name__ == "__main__":
    main()