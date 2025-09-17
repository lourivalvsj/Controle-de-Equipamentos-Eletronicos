"""
Equipment Manager - Equipment Inventory Management System
Sistema de Gerenciamento de Equipamentos Eletrônicos

This module provides the EquipmentManager class for managing a collection of equipment.
"""

import json
import os
from typing import List, Optional, Dict, Any
from equipment import Equipment, EquipmentType, EquipmentStatus


class EquipmentManager:
    """
    Manages a collection of electronic equipment.
    
    Provides functionality to add, remove, update, and query equipment.
    Supports persistence to/from JSON files.
    """
    
    def __init__(self, data_file: str = "equipment_data.json"):
        """
        Initialize the equipment manager.
        
        Args:
            data_file: Path to the JSON file for data persistence
        """
        self.data_file = data_file
        self.equipment: Dict[str, Equipment] = {}
        self.load_data()
    
    def add_equipment(self, equipment: Equipment) -> bool:
        """
        Add equipment to the inventory.
        
        Args:
            equipment: Equipment instance to add
            
        Returns:
            bool: True if successful, False if ID already exists
        """
        if equipment.id in self.equipment:
            return False
        
        self.equipment[equipment.id] = equipment
        self.save_data()
        return True
    
    def remove_equipment(self, equipment_id: str) -> bool:
        """
        Remove equipment from inventory.
        
        Args:
            equipment_id: ID of equipment to remove
            
        Returns:
            bool: True if successful, False if not found
        """
        if equipment_id in self.equipment:
            del self.equipment[equipment_id]
            self.save_data()
            return True
        return False
    
    def get_equipment(self, equipment_id: str) -> Optional[Equipment]:
        """
        Get equipment by ID.
        
        Args:
            equipment_id: ID of equipment to retrieve
            
        Returns:
            Equipment instance or None if not found
        """
        return self.equipment.get(equipment_id)
    
    def list_equipment(self, status: Optional[EquipmentStatus] = None, 
                      equipment_type: Optional[EquipmentType] = None,
                      location: Optional[str] = None) -> List[Equipment]:
        """
        List equipment with optional filters.
        
        Args:
            status: Filter by status (optional)
            equipment_type: Filter by type (optional)
            location: Filter by location (optional)
            
        Returns:
            List of Equipment instances matching filters
        """
        result = list(self.equipment.values())
        
        if status:
            result = [eq for eq in result if eq.status == status]
        
        if equipment_type:
            result = [eq for eq in result if eq.equipment_type == equipment_type]
        
        if location:
            result = [eq for eq in result if location.lower() in eq.location.lower()]
        
        return result
    
    def search_equipment(self, query: str) -> List[Equipment]:
        """
        Search equipment by name, brand, model, or serial number.
        
        Args:
            query: Search query string
            
        Returns:
            List of Equipment instances matching the query
        """
        query = query.lower()
        result = []
        
        for equipment in self.equipment.values():
            if (query in equipment.name.lower() or
                query in equipment.brand.lower() or
                query in equipment.model.lower() or
                query in equipment.serial_number.lower() or
                query in equipment.notes.lower()):
                result.append(equipment)
        
        return result
    
    def get_status_summary(self) -> Dict[str, int]:
        """
        Get summary of equipment by status.
        
        Returns:
            Dictionary with status counts
        """
        summary = {}
        for status in EquipmentStatus:
            summary[status.value] = 0
        
        for equipment in self.equipment.values():
            summary[equipment.status.value] += 1
        
        return summary
    
    def get_type_summary(self) -> Dict[str, int]:
        """
        Get summary of equipment by type.
        
        Returns:
            Dictionary with type counts
        """
        summary = {}
        for eq_type in EquipmentType:
            summary[eq_type.value] = 0
        
        for equipment in self.equipment.values():
            summary[equipment.equipment_type.value] += 1
        
        return summary
    
    def control_equipment(self, equipment_id: str, action: str) -> bool:
        """
        Control equipment (turn on/off, set to standby, etc.).
        
        Args:
            equipment_id: ID of equipment to control
            action: Action to perform ('on', 'off', 'standby', 'maintenance', 'error')
            
        Returns:
            bool: True if successful, False otherwise
        """
        equipment = self.get_equipment(equipment_id)
        if not equipment:
            return False
        
        action = action.lower()
        success = False
        
        if action == 'on':
            success = equipment.turn_on()
        elif action == 'off':
            success = equipment.turn_off()
        elif action == 'standby':
            success = equipment.set_standby()
        elif action == 'maintenance':
            success = equipment.set_maintenance()
        elif action == 'error':
            success = equipment.set_error()
        
        if success:
            self.save_data()
        
        return success
    
    def update_equipment(self, equipment_id: str, **kwargs) -> bool:
        """
        Update equipment information.
        
        Args:
            equipment_id: ID of equipment to update
            **kwargs: Fields to update
            
        Returns:
            bool: True if successful, False if equipment not found
        """
        equipment = self.get_equipment(equipment_id)
        if not equipment:
            return False
        
        equipment.update_info(**kwargs)
        self.save_data()
        return True
    
    def save_data(self) -> None:
        """Save equipment data to JSON file."""
        data = {}
        for eq_id, equipment in self.equipment.items():
            data[eq_id] = equipment.get_info()
        
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self) -> None:
        """Load equipment data from JSON file."""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for eq_id, eq_data in data.items():
                equipment = Equipment.from_dict(eq_data)
                self.equipment[eq_id] = equipment
                
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def export_to_json(self, filename: str) -> bool:
        """
        Export equipment data to a JSON file.
        
        Args:
            filename: Output filename
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data = []
            for equipment in self.equipment.values():
                data.append(equipment.get_info())
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False
    
    def import_from_json(self, filename: str) -> bool:
        """
        Import equipment data from a JSON file.
        
        Args:
            filename: Input filename
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for eq_data in data:
                equipment = Equipment.from_dict(eq_data)
                self.equipment[equipment.id] = equipment
            
            self.save_data()
            return True
        except Exception as e:
            print(f"Error importing data: {e}")
            return False
    
    def get_equipment_count(self) -> int:
        """Get total number of equipment items."""
        return len(self.equipment)
    
    def clear_all(self) -> None:
        """Clear all equipment data."""
        self.equipment.clear()
        self.save_data()