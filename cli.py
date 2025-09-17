#!/usr/bin/env python3
"""
Equipment Control CLI - Command Line Interface
Interface de Linha de Comando para Controle de Equipamentos

This module provides a command-line interface for the equipment control system.
"""

import sys
import argparse
from typing import Optional
from equipment import Equipment, EquipmentType, EquipmentStatus
from equipment_manager import EquipmentManager


class EquipmentCLI:
    """Command Line Interface for Equipment Control System."""
    
    def __init__(self, data_file: str = "equipment_data.json"):
        """Initialize the CLI with equipment manager."""
        self.manager = EquipmentManager(data_file)
    
    def add_equipment(self, args) -> None:
        """Add new equipment."""
        try:
            equipment_type = EquipmentType(args.type)
        except ValueError:
            print(f"Error: Invalid equipment type '{args.type}'")
            print(f"Valid types: {', '.join([t.value for t in EquipmentType])}")
            return
        
        equipment = Equipment(
            equipment_id=args.id,
            name=args.name,
            equipment_type=equipment_type,
            brand=args.brand or "",
            model=args.model or "",
            serial_number=args.serial or "",
            location=args.location or "",
            notes=args.notes or ""
        )
        
        if self.manager.add_equipment(equipment):
            print(f"Equipment '{args.name}' added successfully with ID: {args.id}")
        else:
            print(f"Error: Equipment with ID '{args.id}' already exists")
    
    def remove_equipment(self, args) -> None:
        """Remove equipment."""
        if self.manager.remove_equipment(args.id):
            print(f"Equipment with ID '{args.id}' removed successfully")
        else:
            print(f"Error: Equipment with ID '{args.id}' not found")
    
    def list_equipment(self, args) -> None:
        """List equipment with optional filters."""
        equipment_list = self.manager.list_equipment(
            status=EquipmentStatus(args.status) if args.status else None,
            equipment_type=EquipmentType(args.type) if args.type else None,
            location=args.location
        )
        
        if not equipment_list:
            print("No equipment found matching the criteria.")
            return
        
        print(f"\nFound {len(equipment_list)} equipment(s):")
        print("-" * 80)
        print(f"{'ID':<10} {'Name':<20} {'Type':<12} {'Status':<12} {'Location':<15}")
        print("-" * 80)
        
        for eq in equipment_list:
            print(f"{eq.id:<10} {eq.name:<20} {eq.equipment_type.value:<12} "
                  f"{eq.status.value:<12} {eq.location:<15}")
    
    def show_equipment(self, args) -> None:
        """Show detailed equipment information."""
        equipment = self.manager.get_equipment(args.id)
        if not equipment:
            print(f"Error: Equipment with ID '{args.id}' not found")
            return
        
        info = equipment.get_info()
        print(f"\nEquipment Details:")
        print("-" * 40)
        print(f"ID: {info['id']}")
        print(f"Name: {info['name']}")
        print(f"Type: {info['type']}")
        print(f"Brand: {info['brand']}")
        print(f"Model: {info['model']}")
        print(f"Serial Number: {info['serial_number']}")
        print(f"Location: {info['location']}")
        print(f"Status: {info['status']}")
        print(f"Created: {info['created_at']}")
        print(f"Last Modified: {info['last_modified']}")
        if info['notes']:
            print(f"Notes: {info['notes']}")
    
    def control_equipment(self, args) -> None:
        """Control equipment (turn on/off, etc.)."""
        if self.manager.control_equipment(args.id, args.action):
            print(f"Equipment '{args.id}' {args.action} command executed successfully")
        else:
            print(f"Error: Could not execute '{args.action}' on equipment '{args.id}'")
    
    def search_equipment(self, args) -> None:
        """Search equipment."""
        equipment_list = self.manager.search_equipment(args.query)
        
        if not equipment_list:
            print(f"No equipment found matching '{args.query}'")
            return
        
        print(f"\nFound {len(equipment_list)} equipment(s) matching '{args.query}':")
        print("-" * 80)
        print(f"{'ID':<10} {'Name':<20} {'Type':<12} {'Brand':<12} {'Model':<15}")
        print("-" * 80)
        
        for eq in equipment_list:
            print(f"{eq.id:<10} {eq.name:<20} {eq.equipment_type.value:<12} "
                  f"{eq.brand:<12} {eq.model:<15}")
    
    def show_summary(self, args) -> None:
        """Show equipment summary."""
        status_summary = self.manager.get_status_summary()
        type_summary = self.manager.get_type_summary()
        total_count = self.manager.get_equipment_count()
        
        print(f"\nEquipment Summary")
        print("=" * 40)
        print(f"Total Equipment: {total_count}")
        
        print(f"\nBy Status:")
        print("-" * 20)
        for status, count in status_summary.items():
            if count > 0:
                print(f"{status.capitalize():<15}: {count}")
        
        print(f"\nBy Type:")
        print("-" * 20)
        for eq_type, count in type_summary.items():
            if count > 0:
                print(f"{eq_type.capitalize():<15}: {count}")
    
    def update_equipment(self, args) -> None:
        """Update equipment information."""
        updates = {}
        if args.name:
            updates['name'] = args.name
        if args.brand:
            updates['brand'] = args.brand
        if args.model:
            updates['model'] = args.model
        if args.serial:
            updates['serial_number'] = args.serial
        if args.location:
            updates['location'] = args.location
        if args.notes:
            updates['notes'] = args.notes
        
        if not updates:
            print("No updates specified")
            return
        
        if self.manager.update_equipment(args.id, **updates):
            print(f"Equipment '{args.id}' updated successfully")
        else:
            print(f"Error: Equipment with ID '{args.id}' not found")


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Electronic Equipment Control System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s add --id PC001 --name "Office Computer" --type computer --brand Dell
  %(prog)s list --status on
  %(prog)s control --id PC001 --action on
  %(prog)s search --query "Dell"
  %(prog)s summary
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add equipment command
    add_parser = subparsers.add_parser('add', help='Add new equipment')
    add_parser.add_argument('--id', required=True, help='Equipment ID')
    add_parser.add_argument('--name', required=True, help='Equipment name')
    add_parser.add_argument('--type', required=True, help='Equipment type')
    add_parser.add_argument('--brand', help='Brand/manufacturer')
    add_parser.add_argument('--model', help='Model')
    add_parser.add_argument('--serial', help='Serial number')
    add_parser.add_argument('--location', help='Location')
    add_parser.add_argument('--notes', help='Notes')
    
    # Remove equipment command
    remove_parser = subparsers.add_parser('remove', help='Remove equipment')
    remove_parser.add_argument('--id', required=True, help='Equipment ID')
    
    # List equipment command
    list_parser = subparsers.add_parser('list', help='List equipment')
    list_parser.add_argument('--status', help='Filter by status')
    list_parser.add_argument('--type', help='Filter by type')
    list_parser.add_argument('--location', help='Filter by location')
    
    # Show equipment command
    show_parser = subparsers.add_parser('show', help='Show equipment details')
    show_parser.add_argument('--id', required=True, help='Equipment ID')
    
    # Control equipment command
    control_parser = subparsers.add_parser('control', help='Control equipment')
    control_parser.add_argument('--id', required=True, help='Equipment ID')
    control_parser.add_argument('--action', required=True, 
                               choices=['on', 'off', 'standby', 'maintenance', 'error'],
                               help='Action to perform')
    
    # Search equipment command
    search_parser = subparsers.add_parser('search', help='Search equipment')
    search_parser.add_argument('--query', required=True, help='Search query')
    
    # Summary command
    subparsers.add_parser('summary', help='Show equipment summary')
    
    # Update equipment command
    update_parser = subparsers.add_parser('update', help='Update equipment')
    update_parser.add_argument('--id', required=True, help='Equipment ID')
    update_parser.add_argument('--name', help='Equipment name')
    update_parser.add_argument('--brand', help='Brand/manufacturer')
    update_parser.add_argument('--model', help='Model')
    update_parser.add_argument('--serial', help='Serial number')
    update_parser.add_argument('--location', help='Location')
    update_parser.add_argument('--notes', help='Notes')
    
    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = EquipmentCLI()
    
    # Route commands
    if args.command == 'add':
        cli.add_equipment(args)
    elif args.command == 'remove':
        cli.remove_equipment(args)
    elif args.command == 'list':
        cli.list_equipment(args)
    elif args.command == 'show':
        cli.show_equipment(args)
    elif args.command == 'control':
        cli.control_equipment(args)
    elif args.command == 'search':
        cli.search_equipment(args)
    elif args.command == 'summary':
        cli.show_summary(args)
    elif args.command == 'update':
        cli.update_equipment(args)


if __name__ == '__main__':
    main()