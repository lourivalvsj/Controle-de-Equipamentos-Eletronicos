"""
Equipment Control System - Core Equipment Class
Sistema de Controle de Equipamentos Eletrônicos

This module defines the Equipment class for managing electronic equipment.
"""

import json
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional


class EquipmentStatus(Enum):
    """Equipment status enumeration."""
    OFF = "off"
    ON = "on"
    STANDBY = "standby"
    MAINTENANCE = "maintenance"
    ERROR = "error"


class EquipmentType(Enum):
    """Equipment type enumeration."""
    COMPUTER = "computer"
    PRINTER = "printer"
    MONITOR = "monitor"
    ROUTER = "router"
    SWITCH = "switch"
    SERVER = "server"
    PHONE = "phone"
    TABLET = "tablet"
    PROJECTOR = "projector"
    OTHER = "other"


class Equipment:
    """
    Represents an electronic equipment item.
    
    Attributes:
        id (str): Unique equipment identifier
        name (str): Equipment name
        equipment_type (EquipmentType): Type of equipment
        brand (str): Equipment brand/manufacturer
        model (str): Equipment model
        serial_number (str): Serial number
        location (str): Physical location
        status (EquipmentStatus): Current status
        created_at (datetime): Creation timestamp
        last_modified (datetime): Last modification timestamp
        notes (str): Additional notes
    """
    
    def __init__(self, equipment_id: str, name: str, equipment_type: EquipmentType, 
                 brand: str = "", model: str = "", serial_number: str = "", 
                 location: str = "", notes: str = ""):
        """
        Initialize a new Equipment instance.
        
        Args:
            equipment_id: Unique identifier for the equipment
            name: Display name for the equipment
            equipment_type: Type of equipment
            brand: Brand/manufacturer (optional)
            model: Model name/number (optional)
            serial_number: Serial number (optional)
            location: Physical location (optional)
            notes: Additional notes (optional)
        """
        self.id = equipment_id
        self.name = name
        self.equipment_type = equipment_type
        self.brand = brand
        self.model = model
        self.serial_number = serial_number
        self.location = location
        self.status = EquipmentStatus.OFF
        self.created_at = datetime.now()
        self.last_modified = datetime.now()
        self.notes = notes
    
    def turn_on(self) -> bool:
        """
        Turn on the equipment.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.status in [EquipmentStatus.OFF, EquipmentStatus.STANDBY]:
            self.status = EquipmentStatus.ON
            self.last_modified = datetime.now()
            return True
        return False
    
    def turn_off(self) -> bool:
        """
        Turn off the equipment.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.status == EquipmentStatus.ON:
            self.status = EquipmentStatus.OFF
            self.last_modified = datetime.now()
            return True
        return False
    
    def set_standby(self) -> bool:
        """
        Set equipment to standby mode.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.status == EquipmentStatus.ON:
            self.status = EquipmentStatus.STANDBY
            self.last_modified = datetime.now()
            return True
        return False
    
    def set_maintenance(self) -> bool:
        """
        Set equipment to maintenance mode.
        
        Returns:
            bool: True if successful, False otherwise
        """
        self.status = EquipmentStatus.MAINTENANCE
        self.last_modified = datetime.now()
        return True
    
    def set_error(self) -> bool:
        """
        Set equipment to error state.
        
        Returns:
            bool: True if successful, False otherwise
        """
        self.status = EquipmentStatus.ERROR
        self.last_modified = datetime.now()
        return True
    
    def update_info(self, **kwargs) -> None:
        """
        Update equipment information.
        
        Args:
            **kwargs: Keyword arguments for fields to update
        """
        updatable_fields = ['name', 'brand', 'model', 'serial_number', 'location', 'notes']
        
        for field, value in kwargs.items():
            if field in updatable_fields:
                setattr(self, field, value)
        
        self.last_modified = datetime.now()
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get equipment information as dictionary.
        
        Returns:
            Dict containing equipment information
        """
        return {
            'id': self.id,
            'name': self.name,
            'type': self.equipment_type.value,
            'brand': self.brand,
            'model': self.model,
            'serial_number': self.serial_number,
            'location': self.location,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'last_modified': self.last_modified.isoformat(),
            'notes': self.notes
        }
    
    def to_json(self) -> str:
        """
        Convert equipment to JSON string.
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.get_info(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Equipment':
        """
        Create Equipment instance from dictionary.
        
        Args:
            data: Dictionary containing equipment data
            
        Returns:
            Equipment instance
        """
        equipment = cls(
            equipment_id=data['id'],
            name=data['name'],
            equipment_type=EquipmentType(data['type']),
            brand=data.get('brand', ''),
            model=data.get('model', ''),
            serial_number=data.get('serial_number', ''),
            location=data.get('location', ''),
            notes=data.get('notes', '')
        )
        
        # Set status and timestamps if provided
        if 'status' in data:
            equipment.status = EquipmentStatus(data['status'])
        if 'created_at' in data:
            equipment.created_at = datetime.fromisoformat(data['created_at'])
        if 'last_modified' in data:
            equipment.last_modified = datetime.fromisoformat(data['last_modified'])
            
        return equipment
    
    def __str__(self) -> str:
        """String representation of equipment."""
        return f"{self.name} ({self.equipment_type.value}) - {self.status.value}"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"Equipment(id='{self.id}', name='{self.name}', type='{self.equipment_type.value}', status='{self.status.value}')"