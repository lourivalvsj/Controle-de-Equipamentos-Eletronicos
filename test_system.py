#!/usr/bin/env python3
"""
Test script for Equipment Control System
Script de teste para o Sistema de Controle de Equipamentos

This script demonstrates and tests the basic functionality of the system.
"""

from equipment import Equipment, EquipmentType, EquipmentStatus
from equipment_manager import EquipmentManager


def test_basic_functionality():
    """Test basic system functionality."""
    print("=== Testing Equipment Control System ===\n")
    
    # Create manager with test data file
    manager = EquipmentManager("test_equipment_data.json")
    
    # Clear any existing data
    manager.clear_all()
    
    print("1. Creating sample equipment...")
    
    # Create some sample equipment
    pc1 = Equipment("PC001", "Computador Principal", EquipmentType.COMPUTER, 
                   brand="Dell", model="OptiPlex 7070", location="Sala 101")
    
    pc2 = Equipment("PC002", "Computador Backup", EquipmentType.COMPUTER,
                   brand="HP", model="EliteDesk", location="Sala 102")
    
    printer = Equipment("IMP001", "Impressora Laser", EquipmentType.PRINTER,
                       brand="HP", model="LaserJet Pro", location="Sala 101")
    
    monitor = Equipment("MON001", "Monitor Principal", EquipmentType.MONITOR,
                       brand="Samsung", model="24inch", location="Sala 101")
    
    router = Equipment("NET001", "Roteador Principal", EquipmentType.ROUTER,
                      brand="Cisco", model="ISR4321", location="Data Center")
    
    # Add equipment to manager
    equipment_list = [pc1, pc2, printer, monitor, router]
    for eq in equipment_list:
        success = manager.add_equipment(eq)
        print(f"  ✓ Added {eq.name} ({eq.id}): {'Success' if success else 'Failed'}")
    
    print(f"\nTotal equipment added: {manager.get_equipment_count()}")
    
    print("\n2. Testing equipment control...")
    
    # Test equipment control
    controls = [
        ("PC001", "on"),
        ("MON001", "on"), 
        ("IMP001", "standby"),
        ("NET001", "on"),
        ("PC002", "maintenance")
    ]
    
    for eq_id, action in controls:
        success = manager.control_equipment(eq_id, action)
        equipment = manager.get_equipment(eq_id)
        status = equipment.status.value if equipment else "not found"
        print(f"  ✓ {eq_id} {action}: {'Success' if success else 'Failed'} (Status: {status})")
    
    print("\n3. Testing search functionality...")
    
    # Test search
    search_queries = ["Dell", "HP", "Sala 101", "Principal"]
    for query in search_queries:
        results = manager.search_equipment(query)
        print(f"  ✓ Search '{query}': {len(results)} results")
        for eq in results:
            print(f"    - {eq.name} ({eq.id})")
    
    print("\n4. Testing filtering...")
    
    # Test filtering
    on_equipment = manager.list_equipment(status=EquipmentStatus.ON)
    print(f"  ✓ Equipment ON: {len(on_equipment)} items")
    for eq in on_equipment:
        print(f"    - {eq.name} ({eq.status.value})")
    
    computers = manager.list_equipment(equipment_type=EquipmentType.COMPUTER)
    print(f"  ✓ Computers: {len(computers)} items")
    for eq in computers:
        print(f"    - {eq.name} ({eq.status.value})")
    
    sala101_equipment = manager.list_equipment(location="Sala 101")
    print(f"  ✓ Equipment in 'Sala 101': {len(sala101_equipment)} items")
    for eq in sala101_equipment:
        print(f"    - {eq.name}")
    
    print("\n5. Testing summaries...")
    
    # Test summaries
    status_summary = manager.get_status_summary()
    type_summary = manager.get_type_summary()
    
    print("  ✓ Status Summary:")
    for status, count in status_summary.items():
        if count > 0:
            print(f"    - {status.capitalize()}: {count}")
    
    print("  ✓ Type Summary:")
    for eq_type, count in type_summary.items():
        if count > 0:
            print(f"    - {eq_type.capitalize()}: {count}")
    
    print("\n6. Testing updates...")
    
    # Test updates
    success = manager.update_equipment("PC001", location="Sala 103", notes="Moved to new location")
    print(f"  ✓ Update PC001: {'Success' if success else 'Failed'}")
    
    updated_pc = manager.get_equipment("PC001")
    if updated_pc:
        print(f"    - New location: {updated_pc.location}")
        print(f"    - Notes: {updated_pc.notes}")
    
    print("\n7. Testing equipment details...")
    
    # Show detailed info for one equipment
    pc1_info = manager.get_equipment("PC001")
    if pc1_info:
        print(f"  ✓ Equipment PC001 details:")
        info = pc1_info.get_info()
        for key, value in info.items():
            print(f"    - {key}: {value}")
    
    print("\n=== Test completed successfully! ===")
    
    # Clean up test data
    import os
    if os.path.exists("test_equipment_data.json"):
        os.remove("test_equipment_data.json")
        print("\nTest data file cleaned up.")


def test_cli_examples():
    """Print CLI usage examples."""
    print("\n" + "="*60)
    print("CLI USAGE EXAMPLES")
    print("="*60)
    
    examples = [
        "# Add equipment",
        'python cli.py add --id PC001 --name "Office Computer" --type computer --brand Dell --location "Room 101"',
        "",
        "# List all equipment",
        "python cli.py list",
        "",
        "# List only computers",
        "python cli.py list --type computer",
        "",
        "# List only equipment that is ON",
        "python cli.py list --status on",
        "",
        "# Turn on equipment",
        "python cli.py control --id PC001 --action on",
        "",
        "# Search for Dell equipment",
        'python cli.py search --query "Dell"',
        "",
        "# Show equipment details", 
        "python cli.py show --id PC001",
        "",
        "# Update equipment location",
        'python cli.py update --id PC001 --location "Room 102"',
        "",
        "# Show summary",
        "python cli.py summary",
        "",
        "# Remove equipment",
        "python cli.py remove --id PC001"
    ]
    
    for example in examples:
        print(example)


if __name__ == "__main__":
    test_basic_functionality()
    test_cli_examples()