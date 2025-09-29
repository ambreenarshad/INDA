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

# Set working directory to INDA
cd ~/INDA/VisioGns3 || exit

# Run commands, hide normal output but capture errors
{
    echo "📂 Extracting files..."
    python3 extract_vsdx.py || { echo "❌ Error in extract_vsdx.py"; cat log.txt; exit 1; }

    echo "🖥 Extracting Machine Names..."
    python3 machine_info.py  || { echo "❌ Error in machine_info.py"; cat log.txt; exit 1; }

    echo "📜 Retrieving Details..."
    python3 retrieve_detail.py  || { echo "❌ Error in retrieve_detail.py"; cat log.txt; exit 1; }
    
    echo "📜 Generating Ansible-Playbook..."
    python3 generate_yaml2.py || { echo "❌ Error in generate_yaml2.py"; cat log.txt; exit 1; }

    echo "🔌 Extracting Connection..."
    python3 ListConnections.py  || { echo "❌ Error in ListConnections.py"; cat log.txt; exit 1; }
    python3 addportnumbers.py  || { echo "❌ Error in addportnumbers.py"; cat log.txt; exit 1; }

    echo "📦 Generating Playbook..."
    python3 generatePlaybook.py  || { echo "❌ Error in generatePlaybook.py"; cat log.txt; exit 1; }

    echo "▶️ Running Playbooks..."
    ansible-playbook gns3_topology.yaml  || { echo "❌ Error in gns3_topology.yaml"; cat log.txt; exit 1; }
    ansible-playbook generated_playbook.yml || { echo "❌ Error in generated_playbook.yml"; cat log.txt; exit 1; }

    echo "✅ Successful"
} 2>&1
