#!/bin/bash
set -e  # Exit immediately if any command fails

echo "🔄 Checking if GNS3 server is running..."

# Check if GNS3 server is already running
if ! pgrep -f "gns3server" > /dev/null; then
    echo "🚀 Starting GNS3 server..."
    gns3 &> /dev/null &  # Start GNS3 server in the background silently
    sleep 5  # Wait for the server to initialize
else
    echo "✅ GNS3 server is already running."
fi

# Set working directory
BASE_DIR=~/INDA/VisioGns3
UPLOADS_DIR="$BASE_DIR/uploads"

cd "$BASE_DIR" || exit

echo "➡️ Running retrieve_detail.py"
python3 retrieve_detail.py
# Get the most recent file in uploads
LATEST_FILE=$(ls -t "$UPLOADS_DIR" | head -n 1)
EXT="${LATEST_FILE##*.}"

echo "📂 Latest file detected: $LATEST_FILE"
echo "📑 File extension: $EXT"

case "$EXT" in
  vsdx)
    echo "🖼 Processing VSDX file..."
    cd "$BASE_DIR/vsdx"

    echo "➡️ Running extract_vsdx.py"
    python3 extract_vsdx.py

    echo "➡️ Running machine_info.py"
    python3 machine_info.py

    echo "➡️ Generating Machines YAML"
    python3 generate_machines_yaml.py

    echo "➡️ Running ListConnections.py"
    python3 ListConnections.py

    echo "➡️ Running addportnumbers.py"
    python3 addportnumbers.py

    echo "➡️ Running generatePlaybook.py"
    python3 generate_connections_yaml.py
    ;;
  
  xml)
    echo "🖼 Processing XML file..."
    cd "$BASE_DIR/xml"

    echo "➡️ Running extract_xml.py"
    python3 extract_xml.py

    # Add extra XML-specific steps here
    echo "⚠️ XML pipeline not fully implemented yet"
    ;;

  svg)
    echo "🖼 Processing SVG file..."
    cd "$BASE_DIR/svg"

    echo "➡️ Running extract_svg.py"
    python3 extract_svg.py

    # Add extra SVG-specific steps here
    echo "⚠️ SVG pipeline not fully implemented yet"
    ;;

  *)
    echo "❌ Unsupported file type: $EXT"
    exit 1
    ;;
esac

# Run ansible playbooks from Main_playbooks
cd "$BASE_DIR/Main_playbooks"
echo "▶️ Running Playbooks..."

echo "➡️ Running Gns3_Machines.yaml"
ansible-playbook Gns3_Machines.yaml

echo "➡️ Running Gns3_Connections.yaml"
ansible-playbook Gns3_Connections.yaml

echo "✅ Completed successfully"
