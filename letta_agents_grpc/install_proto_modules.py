#!/usr/bin/env python3

import os
import sys
import site
import shutil
from pathlib import Path

def fix_proto_imports(file_path):
    """Fix imports in generated proto files"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix the import in pb2_grpc.py
    if file_path.name == 'multi_service_pb2_grpc.py':
        content = content.replace(
            'import multi_service_pb2 as multi__service__pb2',
            'from . import multi_service_pb2 as multi__service__pb2'
        )
    
    with open(file_path, 'w') as f:
        f.write(content)

def install_proto_modules():
    """Install proto modules to site-packages for global access"""
    try:
        # Get the source directory (where this script is)
        source_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        
        site_packages = site.getsitepackages()[0]
        target_dir = Path(site_packages) / "letta_agents_grpc"
        
        print(f"Installing proto modules to: {target_dir}")
        
        # Create target directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)
        
        # Files to copy
        files_to_copy = [
            "multi_service_pb2.py",
            "multi_service_pb2_grpc.py",
            "__init__.py"
        ]
        
        # Copy each file
        for file_name in files_to_copy:
            src = source_dir / file_name
            dst = target_dir / file_name
            
            if not src.exists():
                print(f"Warning: Source file {src} not found")
                continue
                
            print(f"Copying {file_name}...")
            shutil.copy2(src, dst)
            
            # Fix imports in the copied file
            fix_proto_imports(dst)
        
        print("\nInstallation complete! Proto modules are now globally accessible.")
        
    except Exception as e:
        print(f"Error during installation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Error: This script requires root privileges to install to site-packages")
        print("Please run with sudo:")
        print("sudo python3 install_proto_modules.py")
        sys.exit(1)
    install_proto_modules()
