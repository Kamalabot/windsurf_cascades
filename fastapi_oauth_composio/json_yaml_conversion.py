import json
import yaml

# File paths
json_file_path = "server_openapi.json"
yaml_file_path = "fastapi_server.yaml"

# Load JSON file
with open(json_file_path, "r") as json_file:
    json_data = json.load(json_file)

# Convert to YAML and save
with open(yaml_file_path, "w") as yaml_file:
    yaml.dump(json_data, yaml_file, default_flow_style=False)

print(f"Converted file saved as {yaml_file_path}")
