"""
RAG Knowledge Base Generator for Network Topology Project
Generates all necessary RAG documents in the knowledge_base2 folder
"""

import os
import json

def create_directory_structure():
    """Create the knowledge_base2 directory structure"""
    # OUTPUT_DIR = "knowledge_base2"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # NLP1 and knowledge_base directories
    NLP_DIR = os.path.join(BASE_DIR, "NLP1")
    OUTPUT_DIR = os.path.join(NLP_DIR, "knowledge_base2")

    # Make sure the directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    subdirs = [
        "topology_patterns",
        "device_specs",
        "connection_rules",
        "terminology",
        "examples"
    ]
    
    # Create base directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Create subdirectories
    for subdir in subdirs:
        os.makedirs(os.path.join(OUTPUT_DIR, subdir), exist_ok=True)
    
    print(f"✓ Created directory structure in {OUTPUT_DIR}/")
    return OUTPUT_DIR


def generate_topology_patterns(OUTPUT_DIR):
    """Generate topology pattern reference documents"""
    
    # Ring/Loop Topology
    ring_content = """# Ring/Loop Topology

## Description
A ring topology connects devices in a circular chain where each device is connected to exactly two neighbors, forming a closed loop.

## Characteristics
- Each device connects to exactly 2 neighbors
- The last device connects back to the first device
- Creates a circular data path
- No central node

## Connection Formula
- For N devices: Exactly N connections
- Connection pattern: Device i → Device (i+1), with Device N → Device 1

## Keywords
- "ring"
- "loop"
- "circular"
- "ring configuration"
- "circular chain"

## Example Patterns
```
3 devices: 1→2, 2→3, 3→1
5 devices: 1→2, 2→3, 3→4, 4→5, 5→1
N devices: 1→2, 2→3, ..., (N-1)→N, N→1
```

## Use Cases
- Token passing networks
- Fault-tolerant systems (can detect breaks)
- Equal access networks
"""

    # Star Topology
    star_content = """# Star Topology

## Description
A star topology features a central device (hub/switch/router) with all other devices connected directly to it, radiating outward like spokes on a wheel.

## Characteristics
- One central device
- All peripheral devices connect only to the center
- No direct connections between peripheral devices
- Central point of failure

## Connection Formula
- For 1 central + N peripheral devices: Exactly N connections
- All connections: Central → Peripheral device

## Keywords
- "star"
- "radiating from"
- "hub-and-spoke"
- "centralized"
- "central hub"

## Example Patterns
```
1 center + 3 peripherals: C→1, C→2, C→3
1 switch + 5 servers: S→S1, S→S2, S→S3, S→S4, S→S5
```

## Use Cases
- Most common LAN topology
- Easy to manage and troubleshoot
- Simple to add/remove devices
"""

    # Tree Topology
    tree_content = """# Tree Topology

## Description
A tree topology is a hierarchical structure with a root device at the top, branch devices in the middle, and leaf devices at the bottom. No loops or redundant paths exist.

## Characteristics
- Hierarchical structure: root → branches → leaves
- Root connects to branch devices
- Branch devices connect to leaf devices
- No loops or redundant connections
- Clear parent-child relationships

## Connection Formula
- Varies based on branching factor
- Each branch can have multiple leaves
- No leaf-to-leaf connections

## Keywords
- "tree"
- "hierarchical"
- "root"
- "branches"
- "leaves"
- "as root"
- "as branches"
- "as leaves"

## Example Patterns
```
1 root, 2 branches, 4 leaves:
  Root → Branch1, Root → Branch2
  Branch1 → Leaf1, Branch1 → Leaf2
  Branch2 → Leaf3, Branch2 → Leaf4
```

## Use Cases
- Enterprise networks
- Scalable architectures
- Clear hierarchy needed
"""

    # Partial Mesh Topology
    partial_mesh_content = """# Partial Mesh Topology

## Description
A partial mesh topology has some devices with multiple connections to other devices, but not all devices are connected to all others. Provides redundancy without full mesh complexity.

## Characteristics
- Some devices have multiple connections
- Not every device connects to every other device
- Provides some redundancy and alternate paths
- More connections than tree, fewer than full mesh
- No fixed pattern - connections vary

## Connection Formula
- Variable: More than (N-1), less than N*(N-1)/2
- Typically 2-4 connections per device on average
- Strategic connections for redundancy

## Keywords
- "partial mesh"
- "redundant"
- "some redundancy"
- "mesh"
- "interconnected"

## Example Patterns
```
5 devices with partial mesh:
  Could have 8-12 connections
  Some devices connect to 2-3 others
  Not all pairs connected
```

## Use Cases
- Redundant networks
- Critical infrastructure
- Balance between cost and reliability
"""

    # Bus Topology
    bus_content = """# Bus/Linear Bus Topology

## Description
A bus topology uses a single backbone (main cable/device) with all other devices connected directly to it. All devices share the same communication medium.

## Characteristics
- Single central backbone/bus
- All devices connect directly to the bus
- One device acts as the bus (router/switch)
- Simple linear structure

## Connection Formula
- For 1 bus + N devices: Exactly N connections
- All connections: Bus → Device

## Keywords
- "bus"
- "linear bus"
- "backbone"
- "using [device] and [N] [devices]"

## Example Patterns
```
1 router + 5 PCs: R→PC1, R→PC2, R→PC3, R→PC4, R→PC5
1 switch + 10 servers: S→S1, S→S2, ..., S→S10
```

## Use Cases
- Simple networks
- Small office setups
- Legacy systems
"""

    # Daisy Chain Topology
    daisy_chain_content = """# Daisy Chain Topology

## Description
A daisy chain topology connects devices in a linear sequence, where each device connects to the next one in line, forming a chain without returning to the start.

## Characteristics
- Linear sequence of connections
- Each device connects to the next (except endpoints)
- First device: only 1 connection (to second)
- Last device: only 1 connection (to second-to-last)
- Middle devices: 2 connections each
- NOT a loop (doesn't connect back)

## Connection Formula
- For N devices: (N-1) connections
- Pattern: 1→2, 2→3, 3→4, ..., (N-1)→N

## Keywords
- "daisy chain"
- "series"
- "sequential"
- "linear"
- "chained"
- "in series"
- "daisy-chained"

## Example Patterns
```
4 devices: 1→2, 2→3, 3→4
7 devices: 1→2, 2→3, 3→4, 4→5, 5→6, 6→7
```

## Additional Pattern: Daisy Chain with Endpoints
- Main chain of devices (e.g., routers)
- Each chain device has additional endpoint connections (e.g., servers)
- Creates a spine-and-leaf variation

## Use Cases
- Simple expansion
- Cable cost reduction
- Controlled data flow
"""

    # Full Mesh Topology
    full_mesh_content = """# Full Mesh Topology

## Description
A full mesh topology connects every device to every other device, creating maximum redundancy and fault tolerance.

## Characteristics
- Every device connects to every other device
- Maximum redundancy
- Highest fault tolerance
- Most expensive and complex

## Connection Formula
- For N devices: N*(N-1)/2 connections
- Each device has (N-1) connections

## Keywords
- "full mesh"
- "fully connected"
- "complete mesh"
- "all-to-all"

## Example Patterns
```
3 devices: 1↔2, 1↔3, 2↔3 (3 connections)
4 devices: 1↔2, 1↔3, 1↔4, 2↔3, 2↔4, 3↔4 (6 connections)
5 devices: 10 connections
```

## Use Cases
- Critical systems requiring maximum uptime
- Small networks where cost isn't primary concern
- High reliability requirements
"""

    # Hybrid/Mixed Topology
    hybrid_content = """# Hybrid/Mixed Topology

## Description
A hybrid topology combines two or more different topology types to create a complex network that leverages advantages of each topology type.

## Characteristics
- Combines multiple topology types
- Can include star, tree, bus, ring elements
- Flexible and scalable
- Common in enterprise networks

## Keywords
- "hybrid"
- "mixed"
- "heterogeneous"
- "complex"
- "multi-tier"
- "layered"

## Common Patterns
- Star-Bus: Multiple star networks connected via bus
- Star-Ring: Multiple star networks in ring configuration
- Tree-Star: Tree topology with star configurations at leaves
- Three-tier: Hierarchical with core, distribution, access layers

## Example Patterns
```
Three-tier network:
  Core: Routers interconnected
  Distribution: Switches connected to routers
  Access: End devices connected to switches
```

## Use Cases
- Enterprise networks
- Campus networks
- Large organizations
- Complex requirements
"""

    # Write all topology pattern files
    patterns = {
        "ring_topology.md": ring_content,
        "star_topology.md": star_content,
        "tree_topology.md": tree_content,
        "partial_mesh_topology.md": partial_mesh_content,
        "bus_topology.md": bus_content,
        "daisy_chain_topology.md": daisy_chain_content,
        "full_mesh_topology.md": full_mesh_content,
        "hybrid_topology.md": hybrid_content
    }
    
    for filename, content in patterns.items():
        filepath = os.path.join(OUTPUT_DIR, "topology_patterns", filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"✓ Generated {len(patterns)} topology pattern documents")


def generate_device_specs(OUTPUT_DIR):
    """Generate device specification documents"""
    
    device_specs = {
        "routers.json": {
            "device_type": "router",
            "description": "Layer 3 network device that forwards packets between networks",
            "naming_convention": "router [number]",
            "examples": ["router 1", "router 2", "router 10"],
            "typical_connections": {
                "can_connect_to": ["router", "switch", "cloud", "server", "hub"],
                "typically_connects_to": ["switch", "cloud", "router"],
                "layer": "Layer 3 (Network Layer)"
            },
            "role_in_topology": {
                "primary": "Core/Distribution layer",
                "can_be_root": True,
                "can_be_branch": True,
                "can_be_leaf": False
            },
            "characteristics": [
                "Routes traffic between networks",
                "Makes forwarding decisions based on IP addresses",
                "Can connect different network segments",
                "Often connects to WAN/Internet (via cloud)"
            ]
        },
        
        "switches.json": {
            "device_type": "switch",
            "description": "Layer 2 network device that forwards frames within a network",
            "naming_convention": "switch [number]",
            "examples": ["switch 1", "switch 2", "switch 10"],
            "typical_connections": {
                "can_connect_to": ["router", "switch", "server", "pc", "laptop", "hub"],
                "typically_connects_to": ["router", "server", "pc", "laptop"],
                "layer": "Layer 2 (Data Link Layer)"
            },
            "role_in_topology": {
                "primary": "Distribution/Access layer",
                "can_be_root": True,
                "can_be_branch": True,
                "can_be_leaf": False
            },
            "characteristics": [
                "Forwards traffic based on MAC addresses",
                "Connects devices in same network segment",
                "Provides multiple ports for end devices",
                "Common in star topology centers"
            ]
        },
        
        "servers.json": {
            "device_type": "server",
            "description": "End device that provides services to other network devices",
            "naming_convention": "server [number]",
            "examples": ["server 1", "server 2", "server 10"],
            "typical_connections": {
                "can_connect_to": ["switch", "router", "hub"],
                "typically_connects_to": ["switch"],
                "layer": "Application Layer (End Device)"
            },
            "role_in_topology": {
                "primary": "Access layer / End device",
                "can_be_root": False,
                "can_be_branch": False,
                "can_be_leaf": True
            },
            "characteristics": [
                "Provides services (web, database, file storage)",
                "End point in topology",
                "Usually connects to switches",
                "Can have redundant connections"
            ]
        },
        
        "pcs.json": {
            "device_type": "pc",
            "description": "Personal computer workstation, end user device",
            "naming_convention": "pc [number]",
            "examples": ["pc 1", "pc 2", "pc 10"],
            "typical_connections": {
                "can_connect_to": ["switch", "hub", "router"],
                "typically_connects_to": ["switch", "hub"],
                "layer": "Application Layer (End Device)"
            },
            "role_in_topology": {
                "primary": "Access layer / End device",
                "can_be_root": False,
                "can_be_branch": False,
                "can_be_leaf": True
            },
            "characteristics": [
                "End user workstation",
                "Client device",
                "Typically has single network connection",
                "Leaf node in topology"
            ]
        },
        
        "laptops.json": {
            "device_type": "laptop",
            "description": "Portable computer workstation, end user device",
            "naming_convention": "laptop [number]",
            "examples": ["laptop 1", "laptop 2", "laptop 10"],
            "typical_connections": {
                "can_connect_to": ["switch", "hub", "router"],
                "typically_connects_to": ["switch", "hub"],
                "layer": "Application Layer (End Device)"
            },
            "role_in_topology": {
                "primary": "Access layer / End device",
                "can_be_root": False,
                "can_be_branch": False,
                "can_be_leaf": True
            },
            "characteristics": [
                "Portable end user device",
                "Client device",
                "Mobile workstation",
                "Leaf node in topology"
            ]
        },
        
        "hubs.json": {
            "device_type": "hub",
            "description": "Basic Layer 1 device that broadcasts to all ports",
            "naming_convention": "hub [number]",
            "examples": ["hub 1", "hub 2", "hub 10"],
            "typical_connections": {
                "can_connect_to": ["switch", "pc", "laptop", "server"],
                "typically_connects_to": ["pc", "laptop", "server"],
                "layer": "Layer 1 (Physical Layer)"
            },
            "role_in_topology": {
                "primary": "Access layer (legacy)",
                "can_be_root": False,
                "can_be_branch": True,
                "can_be_leaf": False
            },
            "characteristics": [
                "Legacy device (mostly replaced by switches)",
                "Broadcasts to all ports",
                "No intelligence",
                "Simple connectivity"
            ]
        },
        
        "clouds.json": {
            "device_type": "cloud",
            "description": "Represents external network, WAN, or Internet connection",
            "naming_convention": "cloud [number]",
            "examples": ["cloud 1", "cloud 2", "cloud 10"],
            "typical_connections": {
                "can_connect_to": ["router"],
                "typically_connects_to": ["router"],
                "layer": "External Network"
            },
            "role_in_topology": {
                "primary": "WAN/Internet entry point",
                "can_be_root": True,
                "can_be_branch": False,
                "can_be_leaf": False
            },
            "characteristics": [
                "Represents Internet or WAN",
                "External network connection",
                "Usually connects to edge routers",
                "Entry/exit point of topology"
            ]
        }
    }
    
    for filename, content in device_specs.items():
        filepath = os.path.join(OUTPUT_DIR, "device_specs", filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2)
    
    print(f"✓ Generated {len(device_specs)} device specification documents")


def generate_connection_rules(OUTPUT_DIR):
    """Generate connection rules and constraints"""
    
    connection_rules_content = """# Network Connection Rules and Constraints

## Hierarchical Connection Patterns

### Standard Network Hierarchy
```
Cloud (Internet/WAN)
  ↓
Router (Core/Edge Layer)
  ↓
Switch (Distribution/Access Layer)
  ↓
End Devices (Servers, PCs, Laptops)
```

### Typical Flow
1. **Cloud → Router**: WAN/Internet entry
2. **Router → Router**: Inter-network routing
3. **Router → Switch**: Distribution to access layer
4. **Switch → Switch**: Redundancy or extended access
5. **Switch → End Devices**: Access layer connectivity
6. **Hub → End Devices**: Legacy access (rare)

## Valid Connection Pairs

### Layer 3 Devices (Routers)
- **Router ↔ Router**: Valid - inter-router connections for routing
- **Router ↔ Switch**: Valid - most common distribution pattern
- **Router ↔ Cloud**: Valid - WAN/Internet connectivity
- **Router ↔ Server**: Valid - direct server connection (less common)
- **Router ↔ Hub**: Valid - legacy configuration

### Layer 2 Devices (Switches)
- **Switch ↔ Switch**: Valid - redundancy, extended access
- **Switch ↔ Router**: Valid - uplink to core
- **Switch ↔ Server**: Valid - most common server connection
- **Switch ↔ PC**: Valid - most common PC connection
- **Switch ↔ Laptop**: Valid - most common laptop connection
- **Switch ↔ Hub**: Valid - legacy extension

### Layer 1 Devices (Hubs)
- **Hub ↔ PC**: Valid - legacy workstation connection
- **Hub ↔ Laptop**: Valid - legacy laptop connection
- **Hub ↔ Server**: Valid - legacy server connection
- **Hub ↔ Switch**: Valid - uplink to better equipment

### End Devices
- **Server ↔ Switch**: Most common
- **Server ↔ Router**: Direct connection (DMZ, special cases)
- **PC ↔ Switch**: Most common
- **PC ↔ Hub**: Legacy
- **Laptop ↔ Switch**: Most common
- **Laptop ↔ Hub**: Legacy

### External Connections
- **Cloud ↔ Router**: Standard WAN/Internet entry point
- **Cloud ↔ Cloud**: Invalid (clouds represent external networks)

## Connection Directionality

### Directional Connections
- Most connections in topology descriptions are **directional**
- Format: `device1 -> device2` means device1 connects TO device2
- In implementation, many are bidirectional for data flow

### Bidirectional Implications
- Physical connections are typically bidirectional
- Data can flow both ways
- In ring/loop topologies, direction matters for token passing

### Special Cases
- **Ring/Loop**: Strictly directional in pattern (1→2→3→...→N→1)
- **Star**: All connections point from center to peripherals
- **Daisy Chain**: Sequential directional (1→2→3→4)
- **Mesh**: Can be bidirectional or specific paths

## Connection Constraints

### Prohibited Patterns
- **End Device ↔ End Device**: Generally not direct
  - PC ↔ PC: No direct connection
  - Server ↔ Server: No direct connection
  - Laptop ↔ Laptop: No direct connection
- **Cloud ↔ End Device**: Clouds don't connect directly to end devices
- **Cloud ↔ Switch**: Typically not direct (goes through router)

### Logical Constraints
- **No Loops** (except ring/loop topology): Tree topologies must be acyclic
- **Single Root**: Tree topologies have one root device
- **Star Center**: Star topology needs exactly one central device
- **Ring Closure**: Ring topology must close (last connects to first)

## Common Network Patterns

### Three-Tier Architecture
```
Core Layer: Routers
  ↓
Distribution Layer: Switches
  ↓
Access Layer: End Devices
```

### DMZ Pattern
```
Internet (Cloud) → Edge Router → DMZ Switch → Public Servers
                              → Internal Network
```

### Redundant Pattern
```
Device A → Primary Path → Device B
        → Backup Path  → Device B
```

## Connection Density Guidelines

### Topology Type vs Connection Count
- **Ring**: N devices = N connections
- **Star**: N peripherals + 1 center = N connections
- **Tree**: N devices ≈ N-1 connections (minimum)
- **Bus**: N devices + 1 bus = N connections
- **Partial Mesh**: N devices = 1.5N to 3N connections (typical)
- **Full Mesh**: N devices = N*(N-1)/2 connections
- **Daisy Chain**: N devices = N-1 connections

## Best Practices

1. **Hierarchical Design**: Follow OSI model layers
2. **Redundancy**: Critical paths should have backups
3. **Scalability**: Design for growth
4. **Simplicity**: Minimize unnecessary complexity
5. **Standards**: Follow industry best practices
"""

    filepath = os.path.join(OUTPUT_DIR, "connection_rules", "connection_patterns.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(connection_rules_content)
    
    # Generate JSON version for programmatic access
    connection_rules_json = {
        "valid_connections": {
            "router": ["router", "switch", "cloud", "server", "hub"],
            "switch": ["router", "switch", "server", "pc", "laptop", "hub"],
            "server": ["switch", "router", "hub"],
            "pc": ["switch", "hub"],
            "laptop": ["switch", "hub"],
            "hub": ["switch", "pc", "laptop", "server"],
            "cloud": ["router"]
        },
        "hierarchical_order": [
            "cloud",
            "router",
            "switch",
            "hub",
            "server",
            "pc",
            "laptop"
        ],
        "connection_formulas": {
            "ring": "N connections for N devices",
            "star": "N connections for 1 center + N peripherals",
            "tree": "N-1 connections for N devices (minimum)",
            "bus": "N connections for 1 bus + N devices",
            "daisy_chain": "N-1 connections for N devices",
            "partial_mesh": "varies, typically 1.5N to 3N connections",
            "full_mesh": "N*(N-1)/2 connections for N devices"
        },
        "prohibited_connections": [
            ["pc", "pc"],
            ["pc", "laptop"],
            ["pc", "server"],
            ["laptop", "laptop"],
            ["laptop", "server"],
            ["server", "server"],
            ["cloud", "cloud"],
            ["cloud", "switch"],
            ["cloud", "pc"],
            ["cloud", "laptop"],
            ["cloud", "server"]
        ]
    }
    
    filepath_json = os.path.join(OUTPUT_DIR, "connection_rules", "connection_rules.json")
    with open(filepath_json, 'w', encoding='utf-8') as f:
        json.dump(connection_rules_json, f, indent=2)
    
    print("✓ Generated connection rules documents")


def generate_terminology(OUTPUT_DIR):
    """Generate terminology and keyword mappings"""
    
    terminology = {
        "topology_synonyms": {
            "ring": ["loop", "circular", "ring configuration", "circular chain", "ring topology"],
            "star": ["radiating from", "hub-and-spoke", "centralized", "star topology", "radial"],
            "tree": ["hierarchical", "root-branch-leaf", "tree topology", "branching"],
            "bus": ["linear bus", "backbone", "bus topology"],
            "mesh": ["fully connected", "interconnected", "complete mesh"],
            "partial_mesh": ["redundant", "some redundancy", "partial mesh", "partially connected"],
            "daisy_chain": ["series", "sequential", "linear", "chained", "daisy-chained", "in series"],
            "hybrid": ["mixed", "heterogeneous", "complex", "multi-tier", "combined"]
        },
        
        "topology_keywords": {
            "ring": ["ring", "loop", "circular"],
            "star": ["radiating", "star", "central"],
            "tree": ["tree", "root", "branches", "leaves", "hierarchical"],
            "bus": ["bus", "linear bus", "backbone"],
            "mesh": ["mesh", "interconnected"],
            "partial_mesh": ["partial mesh", "redundant"],
            "daisy_chain": ["daisy", "series", "sequential", "chain"],
            "hybrid": ["mixed", "heterogeneous", "layered", "multi-tier", "three-tier"]
        },
        
        "device_type_synonyms": {
            "router": ["router", "routers", "R"],
            "switch": ["switch", "switches", "SW"],
            "server": ["server", "servers", "SRV"],
            "pc": ["pc", "pcs", "computer", "computers", "workstation", "workstations"],
            "laptop": ["laptop", "laptops", "notebook", "notebooks"],
            "hub": ["hub", "hubs"],
            "cloud": ["cloud", "clouds", "internet", "wan"]
        },
        
        "connection_phrases": {
            "sequential": ["in series", "daisy-chained", "chained", "sequentially", "one after another"],
            "centralized": ["radiating from", "connected to central", "hub-and-spoke", "emanating from"],
            "hierarchical": ["as root", "as branches", "as leaves", "root at", "with root"],
            "redundant": ["with redundancy", "redundant paths", "backup connections", "multiple paths"],
            "direct": ["directly connected", "point-to-point", "dedicated link"]
        },
        
        "count_phrases": {
            "with": ["with", "having", "using", "containing"],
            "count": ["X devices", "X [device_type]", "[number] [device_type]"]
        },
        
        "structure_keywords": {
            "root": ["root", "top", "head", "main", "primary"],
            "branch": ["branch", "branches", "intermediate", "distribution"],
            "leaf": ["leaf", "leaves", "endpoint", "end device", "terminal"],
            "center": ["center", "central", "hub", "core"],
            "peripheral": ["peripheral", "edge", "outer", "remote"]
        },
        
        "action_verbs": {
            "create": ["create", "build", "make", "construct", "design", "setup", "configure"],
            "connect": ["connect", "link", "attach", "wire", "join", "bridge"],
            "prepare": ["prepare", "setup", "arrange", "organize"]
        },
        
        "quantity_extractors": {
            "patterns": [
                "\\d+\\s+(router|switch|server|pc|laptop|hub|cloud)s?",
                "(router|switch|server|pc|laptop|hub|cloud)\\s+\\d+",
                "with\\s+\\d+\\s+(router|switch|server|pc|laptop|hub|cloud)s?",
                "using\\s+\\d+\\s+(router|switch|server|pc|laptop|hub|cloud)s?"
            ]
        }
    }
    
    filepath = os.path.join(OUTPUT_DIR, "terminology", "network_terminology.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(terminology, f, indent=2)
    
    # Create a glossary in markdown format
    glossary_content = """# Network Topology Terminology Glossary

## Topology Types

### Ring/Loop Topology
- **Keywords**: ring, loop, circular, ring configuration
- **Pattern**: Devices connected in circular chain
- **Characteristics**: Each device connects to 2 neighbors, closed loop

### Star Topology
- **Keywords**: star, radiating from, hub-and-spoke, centralized
- **Pattern**: Central device with peripherals radiating outward
- **Characteristics**: Single central point, all others connect to it

### Tree Topology
- **Keywords**: tree, hierarchical, root, branches, leaves
- **Pattern**: Hierarchical structure with levels
- **Characteristics**: Root device, branch devices, leaf devices

### Bus Topology
- **Keywords**: bus, linear bus, backbone
- **Pattern**: Single backbone with attached devices
- **Characteristics**: One central device, all others connect to it

### Mesh Topology
- **Keywords**: mesh, fully connected, interconnected
- **Pattern**: All devices connected to all others (full mesh)
- **Characteristics**: Maximum redundancy, highest connection count

### Partial Mesh Topology
- **Keywords**: partial mesh, redundant, some redundancy
- **Pattern**: Some redundant connections, not fully connected
- **Characteristics**: Balance between redundancy and complexity

### Daisy Chain Topology
- **Keywords**: daisy chain, series, sequential, chained
- **Pattern**: Linear sequence without closing loop
- **Characteristics**: Each device connects to next, no return to start

### Hybrid/Mixed Topology
- **Keywords**: hybrid, mixed, heterogeneous, multi-tier
- **Pattern**: Combination of multiple topology types
- **Characteristics**: Flexible, complex, uses multiple patterns

## Device Types

### Router
- **Synonyms**: R, gateway
- **Layer**: Layer 3 (Network)
- **Function**: Routes between networks
- **Naming**: router 1, router 2, etc.

### Switch
- **Synonyms**: SW
- **Layer**: Layer 2 (Data Link)
- **Function**: Forwards frames within network
- **Naming**: switch 1, switch 2, etc.

### Server
- **Synonyms**: SRV, host
- **Layer**: Application (End Device)
- **Function**: Provides services
- **Naming**: server 1, server 2, etc.

### PC
- **Synonyms**: computer, workstation, desktop
- **Layer**: Application (End Device)
- **Function**: User workstation
- **Naming**: pc 1, pc 2, etc.

### Laptop
- **Synonyms**: notebook, portable
- **Layer**: Application (End Device)
- **Function**: Portable workstation
- **Naming**: laptop 1, laptop 2, etc.

### Hub
- **Synonyms**: repeater (though technically different)
- **Layer**: Layer 1 (Physical)
- **Function**: Broadcasts to all ports
- **Naming**: hub 1, hub 2, etc.

### Cloud
- **Synonyms**: WAN, Internet
- **Layer**: External Network
- **Function**: Represents external connectivity
- **Naming**: cloud 1, cloud 2, etc.

## Connection Terminology

### Directional Terms
- **Connected to**: General connection
- **Links to**: Connection between devices
- **Attached to**: Physical connection
- **Wired to**: Physical cabling
- **Points to**: Directional connection

### Structural Terms
- **Root**: Top of hierarchy, starting point
- **Branch**: Intermediate level in hierarchy
- **Leaf**: End point, terminal device
- **Center**: Central point in star topology
- **Peripheral**: Outer devices in star topology
- **Backbone**: Main communication path in bus topology
- **Endpoint**: Terminal device or connection end

### Pattern Terms
- **Sequential**: One after another in order
- **Hierarchical**: Organized in levels/tiers
- **Redundant**: Multiple paths for reliability
- **Centralized**: Organized around central point
- **Distributed**: Spread across multiple devices
- **Meshed**: Interconnected with multiple paths

## Quantity Expressions

### Common Formats
- "X routers" (e.g., "5 routers")
- "with X switches" (e.g., "with 3 switches")
- "using X servers" (e.g., "using 10 servers")
- "having X PCs" (e.g., "having 20 PCs")

### Action Verbs
- **Create**: Build new topology
- **Prepare**: Setup topology
- **Design**: Plan topology
- **Configure**: Setup devices
- **Build**: Construct topology
- **Setup**: Arrange devices
"""

    filepath = os.path.join(OUTPUT_DIR, "terminology", "glossary.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(glossary_content)
    
    print("✓ Generated terminology documents")


def generate_examples(OUTPUT_DIR):
    """Generate example topology dataset"""
    
    examples = [
        {
            "prompt": "36 routers in a ring configuration.",
            "machines": [f"router {i}" for i in range(1, 37)],
            "connections": [{"from": f"router {i}", "to": f"router {i+1}"} for i in range(1, 36)] + 
                          [{"from": "router 36", "to": "router 1"}],
            "topology_type": "ring",
            "device_count": 36,
            "connection_count": 36
        },
        {
            "prompt": "Tree topology with switch 1 as root, 2 hubs as branches, and 4 servers as leaves.",
            "machines": ["switch 1", "hub 1", "hub 2", "server 1", "server 2", "server 3", "server 4"],
            "connections": [
                {"from": "switch 1", "to": "hub 1"},
                {"from": "switch 1", "to": "hub 2"},
                {"from": "hub 1", "to": "server 1"},
                {"from": "hub 1", "to": "server 2"},
                {"from": "hub 2", "to": "server 3"},
                {"from": "hub 2", "to": "server 4"}
            ],
            "topology_type": "tree",
            "device_count": 7,
            "connection_count": 6
        },
        {
            "prompt": "31 servers radiating from switch 1.",
            "machines": ["switch 1"] + [f"server {i}" for i in range(1, 32)],
            "connections": [{"from": "switch 1", "to": f"server {i}"} for i in range(1, 32)],
            "topology_type": "star",
            "device_count": 32,
            "connection_count": 31
        },
        {
            "prompt": "partial mesh topology with 19 routers.",
            "machines": [f"router {i}" for i in range(1, 20)],
            "connections": [
                {"from": "router 1", "to": "router 10"},
                {"from": "router 2", "to": "router 16"},
                {"from": "router 3", "to": "router 16"},
                {"from": "router 4", "to": "router 14"},
                {"from": "router 4", "to": "router 5"},
                {"from": "router 4", "to": "router 1"},
                {"from": "router 4", "to": "router 8"},
                {"from": "router 5", "to": "router 8"},
                {"from": "router 6", "to": "router 1"},
                {"from": "router 6", "to": "router 11"},
                {"from": "router 6", "to": "router 10"},
                {"from": "router 7", "to": "router 10"},
                {"from": "router 7", "to": "router 17"},
                {"from": "router 7", "to": "router 12"},
                {"from": "router 8", "to": "router 6"},
                {"from": "router 8", "to": "router 13"},
                {"from": "router 9", "to": "router 19"},
                {"from": "router 10", "to": "router 12"},
                {"from": "router 11", "to": "router 8"},
                {"from": "router 12", "to": "router 13"},
                {"from": "router 13", "to": "router 19"},
                {"from": "router 13", "to": "router 6"},
                {"from": "router 14", "to": "router 17"},
                {"from": "router 14", "to": "router 8"},
                {"from": "router 15", "to": "router 8"},
                {"from": "router 15", "to": "router 11"},
                {"from": "router 15", "to": "router 10"},
                {"from": "router 16", "to": "router 17"},
                {"from": "router 16", "to": "router 11"},
                {"from": "router 17", "to": "router 8"},
                {"from": "router 17", "to": "router 10"},
                {"from": "router 17", "to": "router 19"},
                {"from": "router 17", "to": "router 18"},
                {"from": "router 18", "to": "router 16"},
                {"from": "router 19", "to": "router 4"},
                {"from": "router 19", "to": "router 7"},
                {"from": "router 19", "to": "router 15"}
            ],
            "topology_type": "partial_mesh",
            "device_count": 19,
            "connection_count": 37
        },
        {
            "prompt": "Linear bus using router 1 and 43 pcs.",
            "machines": ["router 1"] + [f"pc {i}" for i in range(1, 44)],
            "connections": [{"from": "router 1", "to": f"pc {i}"} for i in range(1, 44)],
            "topology_type": "bus",
            "device_count": 44,
            "connection_count": 43
        },
        {
            "prompt": "Daisy-chained routers topology with endpoints.",
            "machines": [f"router {i}" for i in range(1, 15)] + [f"server {i}" for i in range(1, 29)],
            "connections": (
                [{"from": f"router {i}", "to": f"router {i+1}"} for i in range(1, 14)] +
                [{"from": f"router {i}", "to": f"server {2*i-1}"} for i in range(1, 15)] +
                [{"from": f"router {i}", "to": f"server {2*i}"} for i in range(1, 15)]
            ),
            "topology_type": "daisy_chain",
            "device_count": 42,
            "connection_count": 41
        },
        {
            "prompt": "Three-tier network with 2 routers, 1 switch, and 20 servers.",
            "machines": ["router 1", "router 2", "switch 1"] + [f"server {i}" for i in range(1, 21)],
            "connections": (
                [{"from": "router 1", "to": "switch 1"}] +
                [{"from": "switch 1", "to": f"server {i}"} for i in range(1, 21)]
            ),
            "topology_type": "tree",
            "device_count": 23,
            "connection_count": 21
        },
        {
            "prompt": "Layered network using 1 router, 2 switches, 18 pcs.",
            "machines": ["router 1", "switch 1", "switch 2"] + [f"pc {i}" for i in range(1, 19)],
            "connections": (
                [{"from": "router 1", "to": "switch 1"}, {"from": "router 1", "to": "switch 2"}] +
                [{"from": "switch 1", "to": f"pc {i}"} for i in range(1, 10)] +
                [{"from": "switch 2", "to": f"pc {i}"} for i in range(10, 19)]
            ),
            "topology_type": "tree",
            "device_count": 21,
            "connection_count": 20
        }
    ]
    
    filepath = os.path.join(OUTPUT_DIR, "examples", "annotated_topologies.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(examples, f, indent=2)
    
    # Create a markdown version with annotations
    md_content = "# Annotated Topology Examples\n\n"
    md_content += "This document contains examples of topology descriptions with their structured outputs.\n\n"
    
    for idx, example in enumerate(examples, 1):
        md_content += f"## Example {idx}: {example['topology_type'].title()} Topology\n\n"
        md_content += f"**Prompt**: {example['prompt']}\n\n"
        md_content += f"**Topology Type**: {example['topology_type']}\n\n"
        md_content += f"**Device Count**: {example['device_count']}\n\n"
        md_content += f"**Connection Count**: {example['connection_count']}\n\n"
        md_content += f"**Machines**: {', '.join(example['machines'][:5])}{'...' if len(example['machines']) > 5 else ''}\n\n"
        md_content += f"**Sample Connections**:\n"
        for conn in example['connections'][:5]:
            md_content += f"- {conn['from']} → {conn['to']}\n"
        if len(example['connections']) > 5:
            md_content += f"- ... ({len(example['connections']) - 5} more connections)\n"
        md_content += "\n---\n\n"
    
    filepath_md = os.path.join(OUTPUT_DIR, "examples", "annotated_examples.md")
    with open(filepath_md, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✓ Generated {len(examples)} example topologies")


def generate_master_index(OUTPUT_DIR):
    """Generate a master index/README for the knowledge base"""
    
    readme_content = """# Network Topology RAG Knowledge Base

This knowledge base contains reference documents for generating network topologies from natural language descriptions.

## Directory Structure

```
knowledge_base2/
├── topology_patterns/      # Topology type definitions and patterns
├── device_specs/          # Network device specifications
├── connection_rules/      # Connection patterns and constraints
├── terminology/           # Keywords, synonyms, and glossary
└── examples/             # Annotated example topologies
```

## Contents

### Topology Patterns
Reference documents for different network topology types:
- Ring/Loop Topology
- Star Topology
- Tree Topology
- Partial Mesh Topology
- Bus/Linear Bus Topology
- Daisy Chain Topology
- Full Mesh Topology
- Hybrid/Mixed Topology

### Device Specifications
Detailed specifications for network devices:
- Routers (Layer 3)
- Switches (Layer 2)
- Servers (End Devices)
- PCs (End Devices)
- Laptops (End Devices)
- Hubs (Layer 1)
- Clouds (External Networks)

### Connection Rules
Rules and constraints for valid network connections:
- Hierarchical connection patterns
- Valid connection pairs
- Connection directionality
- Prohibited patterns
- Best practices

### Terminology
Keywords, synonyms, and terminology mappings:
- Topology type synonyms
- Device type synonyms
- Connection phrases
- Action verbs
- Quantity extractors

### Examples
Annotated example topologies with:
- Natural language prompts
- Structured machine lists
- Connection specifications
- Topology type classifications

## Usage in RAG System

1. **Query Processing**: User provides natural language topology description
2. **Retrieval**: System retrieves relevant documents based on keywords and patterns
3. **Context Building**: Combines retrieved documents with user query
4. **LLM Processing**: LLM generates structured output (machines + connections)
5. **Validation**: Output validated against connection rules
6. **Pipeline Integration**: Structured data passed to topology generation pipeline

## Document Types

- **Markdown (.md)**: Human-readable reference documentation
- **JSON (.json)**: Machine-readable specifications and rules
- Both formats available for maximum flexibility

## Updating the Knowledge Base

To add new topology types or device specifications:
1. Create new document in appropriate subdirectory
2. Follow existing format and structure
3. Add entries to terminology mappings if needed
4. Update this README with new content

## Integration with LLM

These documents serve as context for the LLM to:
- Understand topology patterns
- Recognize device types and naming conventions
- Apply connection rules and constraints
- Parse natural language descriptions
- Generate valid structured outputs

## Version

Knowledge Base Version: 1.0
Generated: 2025
"""

    filepath = os.path.join(OUTPUT_DIR, "README.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✓ Generated master README")


def main():
    """Main function to generate all RAG documents"""
    
    print("\n" + "="*60)
    print("NETWORK TOPOLOGY RAG KNOWLEDGE BASE GENERATOR")
    print("="*60 + "\n")
    
    print("Starting knowledge base generation...\n")
    
    # Create directory structure
    OUTPUT_DIR = create_directory_structure()
    
    # Generate all document types
    print("\nGenerating documents...")
    generate_topology_patterns(OUTPUT_DIR)
    generate_device_specs(OUTPUT_DIR)
    generate_connection_rules(OUTPUT_DIR)
    generate_terminology(OUTPUT_DIR)
    generate_examples(OUTPUT_DIR)
    generate_master_index(OUTPUT_DIR)
    
    print("\n" + "="*60)
    print("GENERATION COMPLETE!")
    print("="*60)
    print(f"\nKnowledge base created in: {OUTPUT_DIR}/")
    print("\nGenerated files:")
    print("  - 8 topology pattern documents")
    print("  - 7 device specification files")
    print("  - 2 connection rule documents")
    print("  - 2 terminology documents")
    print("  - 2 example files (JSON + Markdown)")
    print("  - 1 master README")
    print("\nTotal: 22 files")
    print("\nNext steps:")
    print("  1. Review generated documents")
    print("  2. Customize content as needed")
    print("  3. Create embeddings from documents")
    print("  4. Store embeddings in vector database")
    print("  5. Integrate with LLM pipeline")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()