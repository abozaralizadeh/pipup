#!/usr/bin/env python3
"""
Pipup - Update Python Package versions in requirements.txt

A command-line tool that updates existing packages in requirements.txt
with their exact versions from pip freeze, without adding new packages.
"""

import argparse
import subprocess
import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple


def run_pip_freeze() -> Dict[str, str]:
    """Run pip freeze and return a dictionary of package names and versions."""
    try:
        result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True, check=True)
        packages = {}
        for line in result.stdout.strip().split('\n'):
            if line and '==' in line:
                package, version = line.split('==', 1)
                packages[package.lower()] = version
        return packages
    except subprocess.CalledProcessError as e:
        print(f"Error running pip freeze: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: pip not found. Make sure pip is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)


def get_latest_versions(package_names: List[str]) -> Dict[str, str]:
    """Get the latest versions of packages from PyPI."""
    packages = {}
    
    for package_name in package_names:
        try:
            # Use pip index to get package info
            result = subprocess.run(
                ['pip', 'index', 'versions', package_name], 
                capture_output=True, text=True, check=True
            )
            
            # Parse the output to get the latest version
            # Output format: "package_name (version) Available versions: ..."
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if package_name in line and "(" in line and ")" in line:
                    # Extract the version from the first line
                    version_match = re.search(rf'{package_name} \(([^)]+)\)', line)
                    if version_match:
                        latest_version = version_match.group(1)
                        packages[package_name.lower()] = latest_version
                        break
        except subprocess.CalledProcessError:
            # If pip index fails, try using pip show
            try:
                result = subprocess.run(
                    ['pip', 'show', package_name], 
                    capture_output=True, text=True, check=True
                )
                # Parse the output to get version
                for line in result.stdout.split('\n'):
                    if line.startswith('Version:'):
                        version = line.split(':', 1)[1].strip()
                        packages[package_name.lower()] = version
                        break
            except subprocess.CalledProcessError:
                print(f"Warning: Could not get latest version for {package_name}", file=sys.stderr)
                continue
        except FileNotFoundError:
            print("Error: pip not found. Make sure pip is installed and in your PATH.", file=sys.stderr)
            sys.exit(1)
    
    return packages


def parse_requirements_line(line: str) -> Tuple[str, str, str, str]:
    """
    Parse a requirements.txt line and return (package_name, version_spec, package_with_extras, original_line).
    
    Returns:
        Tuple of (package_name, version_spec, package_with_extras, original_line)
        - package_name: normalized package name (lowercase)
        - version_spec: version specification (e.g., "==1.0.0", ">=1.0.0,<2.0.0")
        - package_with_extras: full package specification with extras (e.g., "flask[async]")
        - original_line: original line with whitespace preserved
    """
    line = line.rstrip('\n')
    original_line = line
    
    # Skip empty lines and comments
    if not line.strip() or line.strip().startswith('#'):
        return None, None, None, original_line
    
    # Handle different version specifiers
    # Match patterns like: package==1.0.0, package>=1.0.0, package<2.0.0, package>=1.0.0,<2.0.0
    version_pattern = r'([a-zA-Z0-9_-]+(?:\[[^\]]+\])?)\s*([=<>!~]+[^#\s]*(?:,\s*[=<>!~]+[^#\s]*)*)'
    match = re.match(version_pattern, line.strip())
    
    if match:
        package_part = match.group(1)
        version_spec = match.group(2)
        
        # Extract package name (remove extras like [async])
        package_name = re.split(r'\[', package_part)[0].lower()
        package_with_extras = package_part.lower()
        
        return package_name, version_spec, package_with_extras, original_line
    else:
        # No version specifier, just package name (may have extras)
        package_part = line.strip().split()[0]
        package_name = re.split(r'\[', package_part)[0].lower()
        package_with_extras = package_part.lower()
        return package_name, None, package_with_extras, original_line


def update_requirements_file(file_path: Path, pip_packages: Dict[str, str], dry_run: bool = False, upgrade_mode: bool = False) -> None:
    """Update the requirements.txt file with exact versions from pip freeze or latest from PyPI."""
    if not file_path.exists():
        print(f"Error: {file_path} not found.", file=sys.stderr)
        sys.exit(1)
    
    # Read current requirements.txt
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    updated_lines = []
    updated_count = 0
    not_found_packages = []
    skip_next = False
    stop_processing = False
    
    # Collect package names for upgrade mode
    package_names_to_upgrade = []
    
    for i, line in enumerate(lines):
        # Check for stop comments first
        if line.strip() in ['#stop-pipup', '#stop-requp']:
            stop_processing = True
            updated_lines.append(line)
            continue
        
        # If we've hit a stop comment, just copy remaining lines
        if stop_processing:
            updated_lines.append(line)
            continue
        
        # Check for skip comments
        if line.strip() in ['#skip-pipup', '#skip-requp']:
            skip_next = True
            updated_lines.append(line)
            continue
        
        package_name, version_spec, package_with_extras, original_line = parse_requirements_line(line)
        
        if package_name is None:
            # Empty line or comment, keep as is
            updated_lines.append(original_line + '\n' if not original_line.endswith('\n') else original_line)
            continue
        
        # If we should skip this package, keep it as is
        if skip_next:
            updated_lines.append(original_line + '\n' if not original_line.endswith('\n') else original_line)
            skip_next = False
            continue
        
        # Collect package names for upgrade mode
        if upgrade_mode:
            package_names_to_upgrade.append(package_name)
    
    # Get latest versions if in upgrade mode
    if upgrade_mode and package_names_to_upgrade:
        print("Getting latest versions from PyPI...")
        pip_packages = get_latest_versions(package_names_to_upgrade)
    
    # Reset for second pass
    updated_lines = []
    skip_next = False
    stop_processing = False
    
    for i, line in enumerate(lines):
        # Check for stop comments first
        if line.strip() in ['#stop-pipup', '#stop-requp']:
            stop_processing = True
            updated_lines.append(line)
            continue
        
        # If we've hit a stop comment, just copy remaining lines
        if stop_processing:
            updated_lines.append(line)
            continue
        
        # Check for skip comments
        if line.strip() in ['#skip-pipup', '#skip-requp']:
            skip_next = True
            updated_lines.append(line)
            continue
        
        package_name, version_spec, package_with_extras, original_line = parse_requirements_line(line)
        
        if package_name is None:
            # Empty line or comment, keep as is
            updated_lines.append(original_line + '\n' if not original_line.endswith('\n') else original_line)
            continue
        
        # If we should skip this package, keep it as is
        if skip_next:
            updated_lines.append(original_line + '\n' if not original_line.endswith('\n') else original_line)
            skip_next = False
            continue
        
        # Check for package with extras first, then base package
        package_to_check = None
        if '[' in original_line and package_with_extras in pip_packages:
            package_to_check = package_with_extras
        elif package_name in pip_packages:
            package_to_check = package_name
        
        if package_to_check and package_to_check in pip_packages:
            # Package found, update with exact version
            new_version = pip_packages[package_to_check]
            # Preserve the original package specification (with or without extras)
            if '[' in original_line:
                # Keep the extras specification
                base_package = re.split(r'\[', original_line.strip())[0]
                new_line = f"{base_package}=={new_version}\n"
            else:
                new_line = f"{package_name}=={new_version}\n"
            updated_lines.append(new_line)
            
            if version_spec != f"=={new_version}":
                updated_count += 1
                if not dry_run:
                    source = "PyPI" if upgrade_mode else "pip freeze"
                    print(f"Updated {package_name}: {version_spec or 'no version'} -> =={new_version} (from {source})")
        else:
            # Package not found, keep original line
            updated_lines.append(original_line + '\n' if not original_line.endswith('\n') else original_line)
            not_found_packages.append(package_name)
            source = "PyPI" if upgrade_mode else "pip freeze"
            print(f"Warning: {package_name} not found in {source}, keeping original specification", file=sys.stderr)
    
    if dry_run:
        print(f"\nDry run: Would update {updated_count} packages")
        if not_found_packages:
            print(f"Packages not found in pip freeze: {', '.join(not_found_packages)}")
        
        # Print the updated requirements.txt content
        print(f"\nUpdated requirements.txt content:")
        print("-" * 50)
        for line in updated_lines:
            print(line.rstrip('\n'))
        print("-" * 50)
        return
    
    # Write updated requirements.txt
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)
    
    print(f"Updated {updated_count} packages in {file_path}")
    if not_found_packages:
        print(f"Packages not found in pip freeze: {', '.join(not_found_packages)}")


def main():
    """Main entry point for the pipup command."""
    parser = argparse.ArgumentParser(
        description="Update Python package versions in requirements.txt with exact versions from pip freeze",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pipup                                    # Update requirements.txt (default)
  pipup --dry-run                          # Show what would be updated
  pipup -U                                 # Update to latest versions from PyPI
  pipup -U --dry-run                       # Preview latest version updates
  pipup requirements.txt                   # Update requirements.txt
  pipup requirements-dev.txt -U            # Update requirements-dev.txt to latest

Skip Conventions:
  #skip-pipup or #skip-requp               # Skip the next package line
  #stop-pipup or #stop-requp               # Skip all remaining lines
        """
    )
    
    parser.add_argument(
        'requirements_file',
        nargs='?',
        default='requirements.txt',
        help='Path to requirements.txt file to update (default: requirements.txt)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be updated without making changes'
    )
    
    parser.add_argument(
        '-U', '--upgrade',
        action='store_true',
        help='Update packages to latest versions from PyPI instead of using pip freeze'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='pipup 1.1.1'
    )
    
    args = parser.parse_args()
    
    requirements_path = Path(args.requirements_file)
    
    if args.upgrade:
        print("Upgrade mode: Getting latest versions from PyPI...")
        pip_packages = {}  # Will be populated in update_requirements_file
    else:
        print("Running pip freeze...")
        pip_packages = run_pip_freeze()
        print(f"Found {len(pip_packages)} installed packages")
    
    print(f"{'Dry run: ' if args.dry_run else ''}Updating {requirements_path}...")
    update_requirements_file(requirements_path, pip_packages, args.dry_run, args.upgrade)
    
    if not args.dry_run:
        print("Done!")


if __name__ == '__main__':
    main()
