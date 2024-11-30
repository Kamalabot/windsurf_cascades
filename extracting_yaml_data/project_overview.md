# YAML Data Extraction Script

## Overview
This script provides functionality to extract and manipulate YAML data from either web-hosted YAML files or local YAML file paths. The script offers an interactive way to view and selectively extract nested key-value pairs from YAML data.

## Features
1. **YAML Source Handling**
   - Support for web-hosted YAML files via URLs
   - Support for local YAML file paths
   - Validation of YAML file sources

2. **Data Visualization**
   - Pretty printing of nested YAML structures
   - Clear visualization of hierarchy levels
   - Formatted output for better readability

3. **Interactive Data Extraction**
   - Selection of specific key-value pairs
   - Support for nested data extraction
   - Flexible output format

## Technical Requirements
- Python 3.7+
- Required packages:
  - `pyyaml`: For YAML parsing
  - `requests`: For fetching web-hosted YAML files
  - `rich`: For pretty printing and formatting

## Usage Example
```bash
# Run the script with a YAML source (file or URL)
./src/yaml_runner.py path/to/file.yaml
# or
./src/yaml_runner.py https://example.com/data.yaml
```

The script provides an interactive menu with the following options:
1. Display YAML structure - Shows the complete YAML hierarchy in a tree format
2. Extract specific data by path - Allows extracting values using dot notation paths
3. Extract by key name - Find all occurrences of a specific key throughout the YAML
4. Exit

### Example Data Extraction
```python
# 1. Path-based extraction:
servers.production.host      # Access nested dictionary values
users[0].name               # Access array elements
config.ports[2]             # Combine dictionary and array access

# 2. Key-based extraction:
# Enter multiple keys separated by commas:
# Input: "host, port, username"
# Example output:
# Key: host
# Path: servers.production.host
# Value: prod.example.com
# Path: servers.staging.host
# Value: staging.example.com
# --------------------------------------------------
# Key: port
# Path: servers.production.port
# Value: 8080
# --------------------------------------------------
# Key: username
# Path: auth.username
# Value: admin

# Results can be saved to a file (default: yaml_extraction_YYYYMMDD_HHMMSS.txt)
```

## Project Structure
```
extracting_yaml_data/
├── requirements.txt        # Project dependencies
├── src/
│   ├── __init__.py
│   └── yaml_runner.py     # Main script with YAMLRunner class
├── tests/
│   ├── __init__.py
│   ├── test_yaml_runner.py
│   └── test_data/
│       └── sample.yaml
└── README.md
```

## Implementation Details
### YAMLRunner Class
The main `YAMLRunner` class provides the following functionality:
1. **YAML Loading**
   - Supports both URL and file path sources
   - Handles web requests and file operations
   - Provides error handling for invalid sources

2. **Data Visualization**
   - Tree-based structure visualization
   - Color-coded output using rich library
   - Clear hierarchy representation

3. **Data Extraction**
   - Interactive path-based value extraction
   - Support for nested dictionary and array access
   - Flexible dot notation syntax

### Dependencies
```
pyyaml>=6.0.1    # YAML parsing
requests>=2.31.0  # URL handling
rich>=13.6.0     # Pretty printing and formatting
```

## Next Steps
1. ~~Create basic project structure~~ ✓
2. ~~Implement core YAML runner~~ ✓
3. Add comprehensive test suite
4. Create sample YAML files
5. Add documentation with more usage examples
