#!/usr/bin/env python3

import argparse
import sys
from typing import Optional, Union
import yaml
import requests
from pathlib import Path
from rich.console import Console
from rich.tree import Tree
from rich.prompt import Prompt, Confirm
from datetime import datetime

class YAMLRunner:
    def __init__(self):
        self.console = Console()
        self.data = None
        
    def load_yaml(self, source: str) -> None:
        """Load YAML data from either a URL or file path."""
        try:
            if source.startswith(('http://', 'https://')):
                response = requests.get(source)
                response.raise_for_status()
                self.data = yaml.safe_load(response.text)
            else:
                with open(source, 'r') as file:
                    self.data = yaml.safe_load(file)
        except (requests.RequestException, yaml.YAMLError, FileNotFoundError) as e:
            self.console.print(f"[red]Error loading YAML: {str(e)}[/red]")
            sys.exit(1)

    def _build_tree(self, data: Union[dict, list], tree: Tree, prefix: str = "") -> None:
        """Recursively build a tree representation of the YAML data."""
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{prefix}.{key}" if prefix else key
                if isinstance(value, (dict, list)):
                    branch = tree.add(f"[yellow]{key}[/yellow]")
                    self._build_tree(value, branch, current_path)
                else:
                    tree.add(f"[yellow]{key}[/yellow]: [green]{value}[/green]")
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                current_path = f"{prefix}[{idx}]"
                if isinstance(item, (dict, list)):
                    branch = tree.add(f"[blue]{idx}[/blue]")
                    self._build_tree(item, branch, current_path)
                else:
                    tree.add(f"[blue]{idx}[/blue]: [green]{item}[/green]")

    def display_structure(self) -> None:
        """Display the YAML structure in a tree format."""
        if not self.data:
            self.console.print("[red]No YAML data loaded![/red]")
            return

        tree = Tree("[bold]YAML Structure[/bold]")
        self._build_tree(self.data, tree)
        self.console.print(tree)

    def _find_key_occurrences(self, data: Union[dict, list], key_name: str, path: str = "") -> list:
        """Find all occurrences of a specific key in the YAML structure."""
        results = []
        
        if isinstance(data, dict):
            for k, v in data.items():
                current_path = f"{path}.{k}" if path else k
                if k == key_name:
                    results.append((current_path, v))
                if isinstance(v, (dict, list)):
                    results.extend(self._find_key_occurrences(v, key_name, current_path))
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                current_path = f"{path}[{idx}]"
                if isinstance(item, (dict, list)):
                    results.extend(self._find_key_occurrences(item, key_name, current_path))
        
        return results

    def extract_by_key(self) -> None:
        """Extract all occurrences of specific keys and optionally save to file."""
        if not self.data:
            self.console.print("[red]No YAML data loaded![/red]")
            return

        # Get multiple keys
        self.console.print("\n[cyan]Enter key names to search for (comma-separated):[/cyan]")
        keys_input = Prompt.ask("Keys")
        key_names = [k.strip() for k in keys_input.split(',')]

        # Collect results for all keys
        all_results = []
        for key_name in key_names:
            results = self._find_key_occurrences(self.data, key_name)
            if results:
                all_results.append((key_name, results))

        if not all_results:
            self.console.print("[red]No occurrences of any specified keys found![/red]")
            return

        # Display results
        total_occurrences = sum(len(results) for _, results in all_results)
        self.console.print(f"\n[cyan]Found {total_occurrences} total occurrence(s):[/cyan]")
        
        # Format results for both display and file
        output_lines = []
        for key_name, results in all_results:
            self.console.print(f"\n[bold yellow]Key: {key_name}[/bold yellow]")
            output_lines.append(f"\nKey: {key_name}")
            
            for path, value in results:
                # Display to console
                self.console.print(f"[yellow]Path:[/yellow] {path}")
                if isinstance(value, (dict, list)):
                    self.console.print_json(data=value)
                    value_str = str(value)
                else:
                    self.console.print(f"[green]Value:[/green] {value}")
                    value_str = str(value)
                
                # Add to file output
                output_lines.append(f"Path: {path}")
                output_lines.append(f"Value: {value_str}")
                output_lines.append("-" * 50)

        # Ask if user wants to save to file
        if Confirm.ask("\nDo you want to save the results to a file?"):
            default_filename = f"yaml_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filename = Prompt.ask("Enter filename", default=default_filename)
            
            try:
                with open(filename, 'w') as f:
                    f.write("\n".join(output_lines))
                self.console.print(f"[green]Results saved to {filename}[/green]")
            except IOError as e:
                self.console.print(f"[red]Error saving to file: {str(e)}[/red]")

def main():
    parser = argparse.ArgumentParser(description="YAML Data Extractor")
    parser.add_argument('source', help='URL or file path to the YAML file')
    args = parser.parse_args()

    runner = YAMLRunner()
    runner.load_yaml(args.source)

    while True:
        console = Console()
        console.print("\n[bold cyan]Choose an option:[/bold cyan]")
        console.print("1. Display YAML structure")
        console.print("2. Extract specific data by path")
        console.print("3. Extract by key name")
        console.print("4. Exit")
        
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4"])
        
        if choice == "1":
            runner.display_structure()
        elif choice == "2":
            runner.extract_data()
        elif choice == "3":
            runner.extract_by_key()
        else:
            break

if __name__ == '__main__':
    main()
