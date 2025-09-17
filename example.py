#!/usr/bin/env python3
"""
Example usage of Equipment Control System
Exemplo de uso do Sistema de Controle de Equipamentos

This script demonstrates how to use the equipment control system programmatically.
"""

from equipment import Equipment, EquipmentType, EquipmentStatus
from equipment_manager import EquipmentManager


def main():
    """Demonstration of the equipment control system."""
    print("=== Equipment Control System Demo ===\n")
    
    # Initialize the equipment manager
    manager = EquipmentManager("demo_equipment.json")
    
    # Clear any existing data for clean demo
    manager.clear_all()
    
    print("1. Adding equipment to inventory...")
    
    # Create and add some equipment
    equipment_list = [
        Equipment("DESK001", "Desktop Principal", EquipmentType.COMPUTER, 
                 brand="Dell", model="OptiPlex 7090", location="Escritório"),
        Equipment("LAP001", "Laptop Portátil", EquipmentType.COMPUTER,
                 brand="Lenovo", model="ThinkPad X1", location="Sala de Reunião"),
        Equipment("IMP001", "Impressora Multifuncional", EquipmentType.PRINTER,
                 brand="HP", model="LaserJet MFP", location="Escritório"),
        Equipment("MON001", "Monitor 4K", EquipmentType.MONITOR,
                 brand="LG", model="27UL500", location="Escritório"),
        Equipment("ROT001", "Roteador Wi-Fi", EquipmentType.ROUTER,
                 brand="TP-Link", model="Archer AX6000", location="Data Center")
    ]
    
    for equipment in equipment_list:
        success = manager.add_equipment(equipment)
        print(f"  ✓ {equipment.name}: {'Adicionado' if success else 'Falhou'}")
    
    print(f"\nTotal de equipamentos: {manager.get_equipment_count()}")
    
    print("\n2. Turning on some equipment...")
    
    # Turn on some equipment
    turn_on_list = ["DESK001", "MON001", "ROT001"]
    for eq_id in turn_on_list:
        success = manager.control_equipment(eq_id, "on")
        equipment = manager.get_equipment(eq_id)
        print(f"  ✓ {equipment.name if equipment else eq_id}: {'Ligado' if success else 'Falhou'}")
    
    print("\n3. Setting some equipment to standby...")
    
    # Set laptop to standby (first turn it on, then standby)
    manager.control_equipment("LAP001", "on")
    success = manager.control_equipment("LAP001", "standby")
    laptop = manager.get_equipment("LAP001")
    print(f"  ✓ {laptop.name}: {'Standby' if success else 'Falhou'}")
    
    print("\n4. Current equipment status:")
    
    # Show all equipment status
    all_equipment = manager.list_equipment()
    for eq in all_equipment:
        print(f"  • {eq.name} ({eq.id}): {eq.status.value} - {eq.location}")
    
    print("\n5. Equipment summary:")
    
    # Show summaries
    status_summary = manager.get_status_summary()
    type_summary = manager.get_type_summary()
    
    print("  Status:")
    for status, count in status_summary.items():
        if count > 0:
            print(f"    - {status}: {count}")
    
    print("  Tipos:")
    for eq_type, count in type_summary.items():
        if count > 0:
            print(f"    - {eq_type}: {count}")
    
    print("\n6. Searching for equipment...")
    
    # Search examples
    searches = [
        ("Dell", "equipamentos Dell"),
        ("Escritório", "equipamentos no escritório"),
        ("Monitor", "monitores")
    ]
    
    for query, description in searches:
        results = manager.search_equipment(query)
        print(f"  ✓ {description}: {len(results)} encontrado(s)")
        for eq in results:
            print(f"    - {eq.name}")
    
    print("\n7. Filtering equipment...")
    
    # Filter examples
    on_equipment = manager.list_equipment(status=EquipmentStatus.ON)
    computers = manager.list_equipment(equipment_type=EquipmentType.COMPUTER)
    office_equipment = manager.list_equipment(location="Escritório")
    
    print(f"  ✓ Equipamentos ligados: {len(on_equipment)}")
    print(f"  ✓ Computadores: {len(computers)}")
    print(f"  ✓ Equipamentos no escritório: {len(office_equipment)}")
    
    print("\n8. Updating equipment information...")
    
    # Update example
    success = manager.update_equipment("DESK001", 
                                     notes="Atualizado com SSD",
                                     location="Escritório - Mesa 1")
    print(f"  ✓ Atualização do DESK001: {'Sucesso' if success else 'Falhou'}")
    
    # Show updated info
    updated = manager.get_equipment("DESK001")
    if updated:
        print(f"    Nova localização: {updated.location}")
        print(f"    Notas: {updated.notes}")
    
    print("\n9. Equipment maintenance scenario...")
    
    # Maintenance scenario
    success = manager.control_equipment("IMP001", "maintenance")
    printer = manager.get_equipment("IMP001")
    print(f"  ✓ {printer.name}: {'Em manutenção' if success else 'Falhou'}")
    
    print("\n10. Final equipment state:")
    
    # Final state
    all_equipment = manager.list_equipment()
    for eq in sorted(all_equipment, key=lambda x: x.id):
        info = eq.get_info()
        print(f"  {info['id']}: {info['name']} [{info['status']}] - {info['location']}")
    
    print(f"\n=== Demo concluído! Total: {manager.get_equipment_count()} equipamentos ===")
    
    # Clean up demo data
    import os
    if os.path.exists("demo_equipment.json"):
        os.remove("demo_equipment.json")
        print("Arquivo de demo removido.")


if __name__ == "__main__":
    main()