import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def extract_machine_names(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    machine_names = []
    for cell in root.findall(".//mxCell"):
        style = cell.get("style", "")
        value = cell.get("value", "").strip()
        if any(keyword in style for keyword in [
            "mxgraph.cisco.routers",
            "mxgraph.cisco.switches",
            "mxgraph.cisco.computers_and_peripherals"
        ]):
            if value:  # If the diagram has a visible label, use it
                machine_names.append(value)
            else:
                # Clean up style: take the first part before ';' or '.'
                base = style.split(";")[0]  # e.g. mxgraph.cisco.routers.atm_router
                base = base.split(".")[-1]  # e.g. atm_router
                machine_names.append(base)
    return machine_names

def select_file_and_extract():
    filepath = filedialog.askopenfilename(
        title="Select an XML file",
        filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
    )
    if not filepath:
        return

    try:
        machines = extract_machine_names(filepath)
        if not machines:
            messagebox.showinfo("Result", "No machines found in the XML.")
            return

        # Always save output in /home/athaar/INDA/VisioGns3/machine_names.txt
        home_dir = os.path.expanduser("~")
        output_dir = os.path.join(home_dir, "INDA", "VisioGns3")
        os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists
        output_path = os.path.join(output_dir, "machine_names.txt")

        with open(output_path, "w") as f:
            for name in machines:
                f.write(name + "\n")

        messagebox.showinfo("Success", f"Machine names saved to:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    select_file_and_extract()
