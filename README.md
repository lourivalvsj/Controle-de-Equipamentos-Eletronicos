# Sistema de Controle de Equipamentos Eletrônicos
## Electronic Equipment Control System

Um sistema completo para gerenciamento e controle de equipamentos eletrônicos, desenvolvido em Python.

A complete system for managing and controlling electronic equipment, developed in Python.

## Funcionalidades / Features

### 🎯 Principais Características / Main Features
- **Gerenciamento de Inventário**: Adicionar, remover e atualizar equipamentos
- **Controle de Status**: Ligar, desligar, standby, manutenção
- **Sistema de Busca**: Buscar equipamentos por diversos critérios
- **Relatórios**: Relatórios de status e tipos de equipamentos
- **Persistência**: Dados salvos em JSON
- **Interface CLI**: Interface de linha de comando completa

- **Inventory Management**: Add, remove and update equipment
- **Status Control**: Turn on/off, standby, maintenance modes
- **Search System**: Search equipment by various criteria
- **Reports**: Status and equipment type reports
- **Persistence**: Data saved in JSON format
- **CLI Interface**: Complete command-line interface

### 🔧 Tipos de Equipamentos Suportados / Supported Equipment Types
- Computadores / Computers
- Impressoras / Printers
- Monitores / Monitors
- Roteadores / Routers
- Switches
- Servidores / Servers
- Telefones / Phones
- Tablets
- Projetores / Projectors
- Outros / Others

### 📊 Status de Equipamentos / Equipment Status
- **Ligado** / On
- **Desligado** / Off
- **Standby**
- **Manutenção** / Maintenance
- **Erro** / Error

## Instalação / Installation

### Pré-requisitos / Prerequisites
- Python 3.6 ou superior / Python 3.6 or higher

### Clone o repositório / Clone the repository
```bash
git clone https://github.com/lourivalvsj/Controle-de-Equipamentos-Eletronicos.git
cd Controle-de-Equipamentos-Eletronicos
```

## Uso / Usage

### Interface de Linha de Comando / Command Line Interface

O sistema fornece uma interface CLI completa através do arquivo `cli.py`.

The system provides a complete CLI interface through the `cli.py` file.

#### Comandos Básicos / Basic Commands

##### Adicionar Equipamento / Add Equipment
```bash
python cli.py add --id PC001 --name "Computador do Escritório" --type computer --brand Dell --model OptiPlex --location "Sala 101"
```

##### Listar Equipamentos / List Equipment
```bash
# Listar todos / List all
python cli.py list

# Filtrar por status / Filter by status
python cli.py list --status on

# Filtrar por tipo / Filter by type
python cli.py list --type computer

# Filtrar por localização / Filter by location
python cli.py list --location "Sala 101"
```

##### Controlar Equipamento / Control Equipment
```bash
# Ligar equipamento / Turn on equipment
python cli.py control --id PC001 --action on

# Desligar equipamento / Turn off equipment
python cli.py control --id PC001 --action off

# Modo standby
python cli.py control --id PC001 --action standby

# Modo manutenção / Maintenance mode
python cli.py control --id PC001 --action maintenance
```

##### Buscar Equipamentos / Search Equipment
```bash
python cli.py search --query "Dell"
python cli.py search --query "Computador"
```

##### Ver Detalhes / View Details
```bash
python cli.py show --id PC001
```

##### Atualizar Equipamento / Update Equipment
```bash
python cli.py update --id PC001 --location "Sala 102" --notes "Transferido para nova sala"
```

##### Relatório / Summary
```bash
python cli.py summary
```

##### Remover Equipamento / Remove Equipment
```bash
python cli.py remove --id PC001
```

### Exemplos de Uso / Usage Examples

#### Exemplo Completo / Complete Example
```bash
# 1. Adicionar alguns equipamentos / Add some equipment
python cli.py add --id PC001 --name "Computador Principal" --type computer --brand Dell --model OptiPlex --location "Sala 101"
python cli.py add --id IMP001 --name "Impressora Laser" --type printer --brand HP --model LaserJet --location "Sala 102"
python cli.py add --id MON001 --name "Monitor 24 polegadas" --type monitor --brand Samsung --location "Sala 101"

# 2. Ligar alguns equipamentos / Turn on some equipment
python cli.py control --id PC001 --action on
python cli.py control --id MON001 --action on

# 3. Ver relatório / View summary
python cli.py summary

# 4. Buscar equipamentos Dell / Search for Dell equipment
python cli.py search --query "Dell"

# 5. Ver detalhes de um equipamento / View equipment details
python cli.py show --id PC001
```

## Estrutura do Projeto / Project Structure

```
Controle-de-Equipamentos-Eletronicos/
├── README.md                 # Documentação / Documentation
├── equipment.py             # Classe Equipment / Equipment class
├── equipment_manager.py     # Gerenciador de equipamentos / Equipment manager
├── cli.py                   # Interface CLI / CLI interface
├── config.json             # Configurações / Configuration
└── equipment_data.json     # Dados persistidos / Persisted data (criado automaticamente / created automatically)
```

## Arquitetura / Architecture

### Classes Principais / Main Classes

#### `Equipment`
Representa um equipamento eletrônico individual com:
- Identificação única (ID, nome, tipo)
- Informações técnicas (marca, modelo, número de série)
- Status atual (ligado, desligado, standby, etc.)
- Localização e notas
- Timestamps de criação e modificação

Represents an individual electronic equipment with:
- Unique identification (ID, name, type)
- Technical information (brand, model, serial number)
- Current status (on, off, standby, etc.)
- Location and notes
- Creation and modification timestamps

#### `EquipmentManager`
Gerencia a coleção de equipamentos:
- Operações CRUD (Create, Read, Update, Delete)
- Busca e filtragem
- Controle de status
- Persistência em JSON
- Relatórios e estatísticas

Manages the equipment collection:
- CRUD operations (Create, Read, Update, Delete)
- Search and filtering
- Status control
- JSON persistence
- Reports and statistics

#### `EquipmentCLI`
Interface de linha de comando:
- Comandos para todas as operações
- Validação de entrada
- Formatação de saída
- Tratamento de erros

Command line interface:
- Commands for all operations
- Input validation
- Output formatting
- Error handling

### Enumerações / Enumerations

#### `EquipmentType`
- computer, printer, monitor, router, switch, server, phone, tablet, projector, other

#### `EquipmentStatus`
- off, on, standby, maintenance, error

## Persistência de Dados / Data Persistence

Os dados são automaticamente salvos em `equipment_data.json` a cada operação que modifica o estado do sistema.

Data is automatically saved to `equipment_data.json` for every operation that modifies the system state.

### Formato dos Dados / Data Format
```json
{
  "PC001": {
    "id": "PC001",
    "name": "Computador Principal",
    "type": "computer",
    "brand": "Dell",
    "model": "OptiPlex",
    "serial_number": "",
    "location": "Sala 101",
    "status": "on",
    "created_at": "2024-01-01T10:00:00",
    "last_modified": "2024-01-01T11:30:00",
    "notes": ""
  }
}
```

## Uso Programático / Programmatic Usage

Além da CLI, você pode usar as classes diretamente em seu código Python:

Besides the CLI, you can use the classes directly in your Python code:

```python
from equipment import Equipment, EquipmentType
from equipment_manager import EquipmentManager

# Criar gerenciador / Create manager
manager = EquipmentManager()

# Adicionar equipamento / Add equipment
pc = Equipment("PC001", "Meu Computador", EquipmentType.COMPUTER)
manager.add_equipment(pc)

# Controlar equipamento / Control equipment
manager.control_equipment("PC001", "on")

# Buscar equipamentos / Search equipment
results = manager.search_equipment("Computador")

# Obter relatório / Get summary
summary = manager.get_status_summary()
```

## Configuração / Configuration

O arquivo `config.json` contém configurações do sistema que podem ser personalizadas conforme necessário.

The `config.json` file contains system configurations that can be customized as needed.

## Contribuição / Contributing

1. Faça um fork do projeto / Fork the project
2. Crie uma branch para sua feature / Create a feature branch
3. Commit suas mudanças / Commit your changes
4. Push para a branch / Push to the branch
5. Abra um Pull Request / Open a Pull Request

## Licença / License

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

This project is under the MIT license. See the LICENSE file for more details.

## Suporte / Support

Para suporte, abra uma issue no GitHub ou entre em contato com os mantenedores do projeto.

For support, open an issue on GitHub or contact the project maintainers.