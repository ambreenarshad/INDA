import random
import json

# Device types
DEVICE_TYPES = ['router', 'switch', 'hub', 'pc', 'laptop', 'server', 'cloud', 'firewall']

# Expanded instruction starters for more variety
INSTRUCTION_STARTERS = [
    'Create a topology with', 'Create a topology having', 'Create a network with',
    'Build a topology with', 'Build a network with', 'Design a topology with',
    'Design a network with', 'Make a topology with', 'Make a network with',
    'Set up a topology with', 'Set up a network with', 'I need a topology with',
    'I want a network with', 'Configure a network with', 'Generate a topology with',
    'Generate a network with', 'Construct a topology with', 'Construct a network with',
    'Develop a topology with', 'Develop a network with', 'Establish a topology with',
    'Establish a network with', 'Form a topology with', 'Form a network with',
    'Arrange a topology with', 'Arrange a network with', 'Organize a topology with',
    'Organize a network with', 'Prepare a topology with', 'Prepare a network with',
    'Create', 'Build', 'Design', 'Make', 'Set up', 'Generate', 'Construct',
    'Develop', 'Establish', 'Form', 'Arrange', 'Organize', 'Prepare',
    'I need', 'I want', 'Can you create', 'Can you build', 'Can you design',
    'Please create', 'Please build', 'Please design', 'Please make',
    'Help me create', 'Help me build', 'Help me design', 'Show me',
    'Give me', 'Provide'
]

CONNECTION_PHRASES = [
    'connected to', 'connected with', 'linked to', 'linked with',
    'attached to', 'wired to', 'plugged into', 'connecting to',
    'linking to', 'hooked up to', 'joined to', 'interfaced with',
    'coupled with', 'bridged to', 'tied to', 'bonded to',
    'networked with', 'interconnected with', 'associated with'
]

# Additional descriptive words for variety
TOPOLOGY_DESCRIPTORS = [
    'simple', 'basic', 'standard', 'typical', 'conventional',
    'complex', 'advanced', 'sophisticated', 'elaborate',
    'scalable', 'flexible', 'robust', 'efficient', 'optimized',
    'secure', 'redundant', 'hierarchical', 'distributed',
    'centralized', 'decentralized', 'hybrid', 'modular'
]

def get_device_name(device_type, number):
    """Generate device name like 'router 1', 'pc 2', etc."""
    return f"{device_type} {number}"

def format_device_list(devices, max_explicit=5):
    """Format device list intelligently"""
    if len(devices) <= max_explicit:
        if len(devices) == 1:
            return devices[0]
        elif len(devices) == 2:
            return f"{devices[0]} and {devices[1]}"
        else:
            return f"{', '.join(devices[:-1])}, and {devices[-1]}"
    else:
        device_type = devices[0].rsplit(' ', 1)[0]
        first_num = devices[0].rsplit(' ', 1)[1]
        last_num = devices[-1].rsplit(' ', 1)[1]
        return f"{device_type}s {first_num} through {last_num}"

def generate_simple_chain_topology():
    """Generate simple chain: Device 1 -> Device 2 -> Device 3"""
    device_type = random.choice(DEVICE_TYPES)
    num_devices = random.randint(2, 50)
   
    machines = [get_device_name(device_type, i) for i in range(1, num_devices + 1)]
    connections = []
   
    for i in range(len(machines) - 1):
        connections.append({"from": machines[i], "to": machines[i + 1]})
   
    conn_phrase = random.choice(CONNECTION_PHRASES)
    starter = random.choice(INSTRUCTION_STARTERS)
    
    # More variety in prompt styles
    if num_devices <= 5:
        prompt_styles = [
            f"{starter} {num_devices} {device_type}s in a chain.",
            f"{starter} {num_devices} {device_type}s {conn_phrase} sequentially.",
            f"{starter} {num_devices} {device_type}s in series.",
            f"Chain {num_devices} {device_type}s together.",
            f"Connect {num_devices} {device_type}s in a linear sequence.",
            f"{num_devices} {device_type}s in a daisy chain configuration.",
        ]
    else:
        prompt_styles = [
            f"{starter} {num_devices} {device_type}s in a chain where each {device_type} is {conn_phrase} the next one.",
            f"Chain {num_devices} {device_type}s sequentially.",
            f"{num_devices} {device_type}s connected in series from {machines[0]} to {machines[-1]}.",
            f"Linear topology with {num_devices} {device_type}s.",
            f"Sequential network of {num_devices} {device_type}s.",
        ]
    
    prompt = random.choice(prompt_styles)
    return {"prompt": prompt, "machines": machines, "connections": connections}

def generate_star_topology():
    """Generate star topology"""
    central_type = random.choice(['router', 'switch', 'hub'])
    peripheral_type = random.choice(['pc', 'laptop', 'server'])
    num_peripherals = random.randint(2, 49)
   
    central = get_device_name(central_type, 1)
    peripherals = [get_device_name(peripheral_type, i) for i in range(1, num_peripherals + 1)]
   
    machines = [central] + peripherals
    connections = [{"from": central, "to": p} for p in peripherals]
   
    conn_phrase = random.choice(CONNECTION_PHRASES)
    descriptor = random.choice(TOPOLOGY_DESCRIPTORS) if random.random() > 0.5 else ""
   
    prompt_styles = [
        f"Star topology with {central} {conn_phrase} {num_peripherals} {peripheral_type}s.",
        f"{descriptor} star network having {central} at center and {num_peripherals} {peripheral_type}s.".strip(),
        f"{central} connecting to {num_peripherals} {peripheral_type}s in star configuration.",
        f"Hub and spoke with {central} and {num_peripherals} {peripheral_type}s.",
        f"{num_peripherals} {peripheral_type}s radiating from {central}.",
    ]
   
    prompt = random.choice(prompt_styles)
    return {"prompt": prompt, "machines": machines, "connections": connections}

def generate_multi_tier_topology():
    """Generate multi-tier topology"""
    num_routers = random.randint(1, 10)
    num_switches = random.randint(1, 15)
    num_end_devices = random.randint(2, 25)
    end_device_type = random.choice(['pc', 'laptop', 'server'])
   
    total = num_routers + num_switches + num_end_devices
    if total > 50:
        ratio = 50 / total
        num_routers = max(1, int(num_routers * ratio))
        num_switches = max(1, int(num_switches * ratio))
        num_end_devices = max(2, 50 - num_routers - num_switches)
   
    routers = [get_device_name('router', i) for i in range(1, num_routers + 1)]
    switches = [get_device_name('switch', i) for i in range(1, num_switches + 1)]
    end_devices = [get_device_name(end_device_type, i) for i in range(1, num_end_devices + 1)]
   
    machines = routers + switches + end_devices
    connections = []
   
    for i, switch in enumerate(switches):
        router = routers[i % len(routers)]
        connections.append({"from": router, "to": switch})
    
    devices_per_switch = len(end_devices) // len(switches)
    for i, switch in enumerate(switches):
        start_idx = i * devices_per_switch
        end_idx = start_idx + devices_per_switch if i < len(switches) - 1 else len(end_devices)
        for device in end_devices[start_idx:end_idx]:
            connections.append({"from": switch, "to": device})
   
    prompt_styles = [
        f"Three-tier network with {num_routers} router{'s' if num_routers > 1 else ''}, {num_switches} switch{'es' if num_switches > 1 else ''}, and {num_end_devices} {end_device_type}s.",
        f"Hierarchical topology: routers at top, switches in middle, {end_device_type}s at bottom.",
        f"Layered network using {num_routers} router{'s' if num_routers > 1 else ''}, {num_switches} switch{'es' if num_switches > 1 else ''}, {num_end_devices} {end_device_type}s.",
        f"Core-distribution-access topology with {num_routers}/{num_switches}/{num_end_devices} devices.",
    ]
   
    prompt = random.choice(prompt_styles)
    return {"prompt": prompt, "machines": machines, "connections": connections}

def generate_mesh_topology():
    """Generate mesh topology"""
    device_type = random.choice(['router', 'switch'])
    num_devices = random.randint(3, 20)
    is_full_mesh = random.choice([True, False])
   
    machines = [get_device_name(device_type, i) for i in range(1, num_devices + 1)]
    connections = []
   
    if is_full_mesh:
        for i in range(len(machines)):
            for j in range(i + 1, len(machines)):
                connections.append({"from": machines[i], "to": machines[j]})
    else:
        for i in range(len(machines)):
            num_connections = random.randint(1, min(4, len(machines) - 1))
            possible_targets = [m for m in machines if m != machines[i]]
            targets = random.sample(possible_targets, min(num_connections, len(possible_targets)))
            for target in targets:
                conn = {"from": machines[i], "to": target}
                reverse_conn = {"from": target, "to": machines[i]}
                if conn not in connections and reverse_conn not in connections:
                    connections.append(conn)
   
    mesh_type = "full mesh" if is_full_mesh else "partial mesh"
    descriptor = random.choice(TOPOLOGY_DESCRIPTORS) if random.random() > 0.5 else ""
   
    prompt_styles = [
        f"{mesh_type} topology with {num_devices} {device_type}s.",
        f"{descriptor} {mesh_type} having {num_devices} {device_type}s.".strip(),
        f"{num_devices} {device_type}s in {mesh_type} configuration.",
        f"Redundant {mesh_type} network using {num_devices} {device_type}s.",
    ]
   
    prompt = random.choice(prompt_styles)
    return {"prompt": prompt, "machines": machines, "connections": connections}

def generate_ring_topology():
    """Generate ring topology"""
    device_type = random.choice(['router', 'switch', 'hub'])
    num_devices = random.randint(3, 50)
   
    machines = [get_device_name(device_type, i) for i in range(1, num_devices + 1)]
    connections = []
   
    for i in range(len(machines)):
        next_i = (i + 1) % len(machines)
        connections.append({"from": machines[i], "to": machines[next_i]})
   
    prompt_styles = [
        f"Ring topology with {num_devices} {device_type}s.",
        f"Circular network having {num_devices} {device_type}s.",
        f"{num_devices} {device_type}s in a ring configuration.",
        f"Loop topology using {num_devices} {device_type}s.",
        f"Closed loop with {num_devices} {device_type}s.",
    ]
   
    prompt = random.choice(prompt_styles)
    return {"prompt": prompt, "machines": machines, "connections": connections}

def generate_mixed_device_topology():
    """Generate topology with various device types"""
    num_routers = random.randint(1, 10)
    num_switches = random.randint(1, 15)
    num_pcs = random.randint(1, 15)
    num_servers = random.randint(0, 10)
    num_clouds = random.randint(0, 5)
    num_laptops = random.randint(0, 10)
    num_hubs = random.randint(0, 5)
   
    total = num_routers + num_switches + num_pcs + num_servers + num_clouds + num_laptops + num_hubs
    if total > 50:
        ratio = 50 / total
        num_routers = max(1, int(num_routers * ratio))
        num_switches = max(1, int(num_switches * ratio))
        num_pcs = max(1, int(num_pcs * ratio))
        num_servers = int(num_servers * ratio)
        num_clouds = int(num_clouds * ratio)
        num_laptops = int(num_laptops * ratio)
        num_hubs = int(num_hubs * ratio)
   
    machines = []
    machines.extend([get_device_name('router', i) for i in range(1, num_routers + 1)])
    machines.extend([get_device_name('switch', i) for i in range(1, num_switches + 1)])
    machines.extend([get_device_name('pc', i) for i in range(1, num_pcs + 1)])
    if num_servers > 0:
        machines.extend([get_device_name('server', i) for i in range(1, num_servers + 1)])
    if num_clouds > 0:
        machines.extend([get_device_name('cloud', i) for i in range(1, num_clouds + 1)])
    if num_laptops > 0:
        machines.extend([get_device_name('laptop', i) for i in range(1, num_laptops + 1)])
    if num_hubs > 0:
        machines.extend([get_device_name('hub', i) for i in range(1, num_hubs + 1)])
   
    connections = []
    routers = [m for m in machines if 'router' in m]
    switches = [m for m in machines if 'switch' in m]
    pcs = [m for m in machines if 'pc' in m]
    servers = [m for m in machines if 'server' in m]
    clouds = [m for m in machines if 'cloud' in m]
    laptops = [m for m in machines if 'laptop' in m]
    hubs = [m for m in machines if 'hub' in m]
   
    if clouds and routers:
        connections.append({"from": clouds[0], "to": routers[0]})
   
    for i, switch in enumerate(switches):
        router = routers[i % len(routers)] if routers else None
        if router:
            connections.append({"from": router, "to": switch})
   
    all_endpoints = pcs + servers + laptops
    for i, endpoint in enumerate(all_endpoints):
        switch = switches[i % len(switches)] if switches else routers[0]
        connections.append({"from": switch, "to": endpoint})
    
    for hub in hubs:
        if switches:
            connections.append({"from": switches[0], "to": hub})
   
    device_counts = []
    if num_routers > 0:
        device_counts.append(f"{num_routers} router{'s' if num_routers > 1 else ''}")
    if num_switches > 0:
        device_counts.append(f"{num_switches} switch{'es' if num_switches > 1 else ''}")
    if num_pcs > 0:
        device_counts.append(f"{num_pcs} PC{'s' if num_pcs > 1 else ''}")
    if num_servers > 0:
        device_counts.append(f"{num_servers} server{'s' if num_servers > 1 else ''}")
    if num_clouds > 0:
        device_counts.append(f"{num_clouds} cloud{'s' if num_clouds > 1 else ''}")
    if num_laptops > 0:
        device_counts.append(f"{num_laptops} laptop{'s' if num_laptops > 1 else ''}")
    if num_hubs > 0:
        device_counts.append(f"{num_hubs} hub{'s' if num_hubs > 1 else ''}")
   
    prompt_styles = [
        f"Network with {', '.join(device_counts)}.",
        f"Mixed topology having {', '.join(device_counts)}.",
        f"Enterprise network using {', '.join(device_counts)}.",
        f"Heterogeneous network with {', '.join(device_counts)}.",
    ]
   
    prompt = random.choice(prompt_styles)
    return {"prompt": prompt, "machines": machines, "connections": connections}

def generate_bus_topology():
    """Generate bus topology"""
    device_type = random.choice(['pc', 'laptop', 'server'])
    num_devices = random.randint(3, 50)
    backbone_type = random.choice(['router', 'switch'])
    
    backbone = get_device_name(backbone_type, 1)
    devices = [get_device_name(device_type, i) for i in range(1, num_devices + 1)]
    
    machines = [backbone] + devices
    connections = [{"from": backbone, "to": device} for device in devices]
    
    prompt_styles = [
        f"Bus topology with {backbone} as backbone and {num_devices} {device_type}s.",
        f"{num_devices} {device_type}s connected to {backbone} in bus configuration.",
        f"Linear bus using {backbone} and {num_devices} {device_type}s.",
    ]
    
    prompt = random.choice(prompt_styles)
    return {"prompt": prompt, "machines": machines, "connections": connections}

def generate_tree_topology():
    """Generate tree topology"""
    root_type = random.choice(['router', 'switch'])
    branch_type = 'switch' if root_type == 'router' else 'hub'
    leaf_type = random.choice(['pc', 'laptop', 'server'])
    
    num_branches = random.randint(2, 8)
    leaves_per_branch = random.randint(2, 6)
    
    total = 1 + num_branches + (num_branches * leaves_per_branch)
    if total > 50:
        num_branches = min(num_branches, 8)
        leaves_per_branch = min(leaves_per_branch, (49 - num_branches) // num_branches)
    
    root = get_device_name(root_type, 1)
    branches = [get_device_name(branch_type, i) for i in range(1, num_branches + 1)]
    leaves = [get_device_name(leaf_type, i) for i in range(1, num_branches * leaves_per_branch + 1)]
    
    machines = [root] + branches + leaves
    connections = []
    
    for branch in branches:
        connections.append({"from": root, "to": branch})
    
    for i, branch in enumerate(branches):
        start_idx = i * leaves_per_branch
        end_idx = start_idx + leaves_per_branch
        for leaf in leaves[start_idx:end_idx]:
            connections.append({"from": branch, "to": leaf})
    
    prompt_styles = [
        f"Tree topology with {root} as root, {num_branches} {branch_type}s as branches, and {len(leaves)} {leaf_type}s as leaves.",
        f"Hierarchical tree having {root} at top with {num_branches} branches.",
        f"Tree network using {root}, {num_branches} {branch_type}s, and {len(leaves)} {leaf_type}s.",
    ]
    
    prompt = random.choice(prompt_styles)
    return {"prompt": prompt, "machines": machines, "connections": connections}

def generate_point_to_point_topology():
    """Generate simple point-to-point connections"""
    num_pairs = random.randint(1, 25)
    device_type1 = random.choice(DEVICE_TYPES)
    device_type2 = random.choice(DEVICE_TYPES)
    
    machines = []
    connections = []
    
    for i in range(1, num_pairs + 1):
        device1 = get_device_name(device_type1, i)
        device2 = get_device_name(device_type2, i)
        machines.extend([device1, device2])
        connections.append({"from": device1, "to": device2})
    
    prompt_styles = [
        f"{num_pairs} point-to-point connections between {device_type1}s and {device_type2}s.",
        f"Point-to-point topology with {num_pairs} pairs of {device_type1}s and {device_type2}s.",
        f"{num_pairs} direct connections from {device_type1}s to {device_type2}s.",
    ]
    
    prompt = random.choice(prompt_styles)
    return {"prompt": prompt, "machines": machines, "connections": connections}

def generate_hybrid_topology():
    """Generate hybrid topology combining multiple patterns"""
    central_type = random.choice(['router', 'switch'])
    star_devices = random.randint(3, 10)
    ring_devices = random.randint(3, 10)
    
    total = 1 + star_devices + ring_devices
    if total > 50:
        ratio = 50 / total
        star_devices = max(3, int(star_devices * ratio))
        ring_devices = 50 - 1 - star_devices
    
    central = get_device_name(central_type, 1)
    star = [get_device_name('pc', i) for i in range(1, star_devices + 1)]
    ring = [get_device_name('switch', i) for i in range(1, ring_devices + 1)]
    
    machines = [central] + star + ring
    connections = []
    
    for device in star:
        connections.append({"from": central, "to": device})
    
    connections.append({"from": central, "to": ring[0]})
    for i in range(len(ring)):
        next_i = (i + 1) % len(ring)
        connections.append({"from": ring[i], "to": ring[next_i]})
    
    prompt_styles = [
        f"Hybrid topology combining star and ring with {central} as hub.",
        f"Star-ring hybrid using {central}, {star_devices} PCs, and {ring_devices} switches.",
        f"Mixed star and ring topology with {total} devices.",
    ]
    
    prompt = random.choice(prompt_styles)
    return {"prompt": prompt, "machines": machines, "connections": connections}

def generate_cascaded_topology():
    """Generate cascaded switches/routers"""
    device_type = random.choice(['switch', 'router'])
    num_cascade = random.randint(3, 15)
    endpoints_per = random.randint(2, 5)
    endpoint_type = random.choice(['pc', 'laptop', 'server'])
    
    total = num_cascade + (num_cascade * endpoints_per)
    if total > 50:
        ratio = 50 / total
        num_cascade = max(3, int(num_cascade * ratio))
        endpoints_per = max(2, (50 - num_cascade) // num_cascade)
    
    cascade = [get_device_name(device_type, i) for i in range(1, num_cascade + 1)]
    endpoints = [get_device_name(endpoint_type, i) for i in range(1, num_cascade * endpoints_per + 1)]
    
    machines = cascade + endpoints
    connections = []
    
    for i in range(len(cascade) - 1):
        connections.append({"from": cascade[i], "to": cascade[i + 1]})
    
    for i, device in enumerate(cascade):
        start_idx = i * endpoints_per
        end_idx = start_idx + endpoints_per
        for endpoint in endpoints[start_idx:end_idx]:
            connections.append({"from": device, "to": endpoint})
    
    prompt_styles = [
        f"Cascaded {device_type}s with {num_cascade} {device_type}s and {len(endpoints)} {endpoint_type}s.",
        f"{num_cascade} {device_type}s in cascade, each with {endpoints_per} {endpoint_type}s.",
        f"Daisy-chained {device_type}s topology with endpoints.",
    ]
    
    prompt = random.choice(prompt_styles)
    return {"prompt": prompt, "machines": machines, "connections": connections}

def generate_dataset(num_samples=20000):
    """Generate the complete dataset"""
    dataset = []
   
    generators = [
        (generate_simple_chain_topology, 2500),
        (generate_star_topology, 2500),
        (generate_multi_tier_topology, 2500),
        (generate_mesh_topology, 2000),
        (generate_ring_topology, 2000),
        (generate_mixed_device_topology, 2500),
        (generate_bus_topology, 1500),
        (generate_tree_topology, 1500),
        (generate_point_to_point_topology, 1000),
        (generate_hybrid_topology, 1000),
        (generate_cascaded_topology, 1000),
    ]
   
    for generator, count in generators:
        for _ in range(count):
            try:
                sample = generator()
                if len(sample['machines']) <= 50:
                    dataset.append(sample)
            except Exception as e:
                print(f"Error generating sample: {e}")
                continue
   
    random.shuffle(dataset)
    return dataset

def save_dataset(dataset, filename='network_topology_dataset_20k.json'):
    """Save dataset to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
   
    print(f"\n{'='*80}")
    print(f"DATASET SAVED SUCCESSFULLY")
    print(f"{'='*80}")
    print(f"Filename: {filename}")
    print(f"Total samples: {len(dataset)}")
    print(f"{'='*80}\n")

def print_statistics(dataset):
    """Print dataset statistics"""
    print(f"\n{'='*80}")
    print("DATASET STATISTICS")
    print(f"{'='*80}")
   
    total_machines = sum(len(sample['machines']) for sample in dataset)
    total_connections = sum(len(sample['connections']) for sample in dataset)
   
    print(f"Total samples: {len(dataset)}")
    print(f"Total machines: {total_machines}")
    print(f"Total connections: {total_connections}")
    print(f"Average machines per sample: {total_machines / len(dataset):.2f}")
    print(f"Average connections per sample: {total_connections / len(dataset):.2f}")
    
    machine_counts = [len(sample['machines']) for sample in dataset]
    print(f"Min machines per topology: {min(machine_counts)}")
    print(f"Max machines per topology: {max(machine_counts)}")
   
    device_counts = {}
    for sample in dataset:
        for machine in sample['machines']:
            device_type = machine.split()[0]
            device_counts[device_type] = device_counts.get(device_type, 0) + 1
   
    print(f"\nDevice type distribution:")
    for device_type, count in sorted(device_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {device_type}: {count} instances")
   
    print(f"{'='*80}\n")

def print_samples(dataset, num_samples=15):
    """Print sample data"""
    print(f"\n{'='*80}")
    print(f"SAMPLE DATA ({num_samples} examples)")
    print(f"{'='*80}\n")
   
    for i, sample in enumerate(random.sample(dataset, min(num_samples, len(dataset))), 1):
        print(f"Sample {i}:")
        print(f"Prompt: {sample['prompt']}")
        print(f"Machines ({len(sample['machines'])}): {sample['machines'][:5]}{'...' if len(sample['machines']) > 5 else ''}")
        print(f"Connections ({len(sample['connections'])}): {sample['connections'][:3]}{'...' if len(sample['connections']) > 3 else ''}")
        print(f"{'-'*80}\n")

if __name__ == "__main__":
    print("="*80)
    print("ENHANCED NETWORK TOPOLOGY DATASET GENERATOR")
    print("="*80)
    print("\nGenerating 20,000 network topology samples...")
    print("Maximum devices per topology: 50")
    print("-" * 80)
   
    dataset = generate_dataset(num_samples=20000)
   
    print_samples(dataset, num_samples=15)
    print_statistics(dataset)
    save_dataset(dataset, filename='network_topology_dataset_20k.json')
   
    print("✅ Dataset generation complete!")
    print(f"{'='*80}\n")