"""
Laptop Transfer Inventory Script
Creates detailed report of current system configuration for transfer to new laptop

Run this on OLD laptop to document everything before transfer
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

print("\n" + "=" * 80)
print("LAPTOP TRANSFER INVENTORY")
print("=" * 80)
print(f"\nGenerating inventory report at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

report_lines = []

def add_section(title):
    report_lines.append("\n" + "=" * 80)
    report_lines.append(title)
    report_lines.append("=" * 80 + "\n")

def add_item(item):
    report_lines.append(item)

# Header
add_section("LAPTOP TRANSFER INVENTORY REPORT")
add_item(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
add_item(f"Computer: {os.environ.get('COMPUTERNAME', 'Unknown')}")
add_item(f"User: {os.environ.get('USERNAME', 'Unknown')}")

# Python Configuration
add_section("PYTHON CONFIGURATION")
print("\n[1] Checking Python configuration...")
add_item(f"Python Version: {sys.version}")
add_item(f"Python Executable: {sys.executable}")

# Installed Packages
print("[2] Listing installed Python packages...")
try:
    result = subprocess.run([sys.executable, "-m", "pip", "list"],
                          capture_output=True, text=True)
    packages = result.stdout
    add_section("INSTALLED PYTHON PACKAGES")
    add_item(packages)
except Exception as e:
    add_item(f"ERROR getting packages: {e}")

# VS Code Extensions
print("[3] Checking VS Code extensions...")
add_section("VS CODE EXTENSIONS")
try:
    # Try to get VS Code extensions
    result = subprocess.run(["code", "--list-extensions"],
                          capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        extensions = result.stdout.strip().split('\n')
        for ext in extensions:
            add_item(f"  - {ext}")
    else:
        add_item("VS Code not found or not in PATH")
except Exception as e:
    add_item(f"Could not list VS Code extensions: {e}")

# Git Configuration
print("[4] Checking Git configuration...")
add_section("GIT CONFIGURATION")
try:
    result = subprocess.run(["git", "config", "--global", "--list"],
                          capture_output=True, text=True)
    if result.returncode == 0:
        add_item(result.stdout)
    else:
        add_item("Git not configured or not installed")
except Exception as e:
    add_item(f"Git not found: {e}")

# Sentinel Configuration
print("[5] Analyzing Sentinel configuration...")
add_section("SENTINEL CONFIGURATION")

sentinel_root = Path(__file__).parent
add_item(f"Sentinel Location: {sentinel_root}")

# Check database
db_path = sentinel_root / "sentinel.db"
if db_path.exists():
    size_mb = db_path.stat().st_size / (1024 * 1024)
    add_item(f"Database: sentinel.db ({size_mb:.2f} MB)")
else:
    add_item("Database: sentinel.db NOT FOUND [CRITICAL]")

# Check config
config_path = sentinel_root / "config.py"
if config_path.exists():
    add_item("Config: config.py EXISTS [CONTAINS API KEYS]")
    # Count non-blank lines to estimate if populated
    with open(config_path, 'r') as f:
        lines = [l for l in f.readlines() if l.strip()]
        add_item(f"  Lines: {len(lines)}")
else:
    add_item("Config: config.py NOT FOUND [CRITICAL]")

# Check virtual environment
venv_path = sentinel_root / "venv"
if venv_path.exists():
    add_item("Virtual Environment: venv\\ EXISTS")
else:
    add_item("Virtual Environment: venv\\ NOT FOUND")

# Check departments
departments = sentinel_root / "Departments"
if departments.exists():
    dept_count = len([d for d in departments.iterdir() if d.is_dir()])
    add_item(f"Departments: {dept_count} folders found")
else:
    add_item("Departments: NOT FOUND [CRITICAL]")

# OneDrive Status
print("[6] Checking OneDrive status...")
add_section("ONEDRIVE STATUS")
onedrive_path = Path(os.environ.get('OneDrive', 'Not Set'))
add_item(f"OneDrive Path: {onedrive_path}")

if "OneDrive" in str(sentinel_root):
    add_item("Sentinel is IN OneDrive (will auto-sync to new laptop)")
else:
    add_item("Sentinel is NOT in OneDrive (must copy manually)")

# File Counts
print("[7] Counting files...")
add_section("FILE INVENTORY")
py_files = list(sentinel_root.rglob("*.py"))
md_files = list(sentinel_root.rglob("*.md"))
json_files = list(sentinel_root.rglob("*.json"))

add_item(f"Python files: {len(py_files)}")
add_item(f"Markdown files: {len(md_files)}")
add_item(f"JSON files: {len(json_files)}")

# Critical Files Checklist
add_section("CRITICAL FILES CHECKLIST")
critical_files = {
    'sentinel.db': sentinel_root / 'sentinel.db',
    'config.py': sentinel_root / 'config.py',
    'requirements.txt': sentinel_root / 'requirements.txt',
    'sentinel_control_panel.py': sentinel_root / 'sentinel_control_panel.py',
}

for name, path in critical_files.items():
    status = "OK" if path.exists() else "MISSING"
    add_item(f"  [{status}] {name}")

# Transfer Recommendations
add_section("TRANSFER RECOMMENDATIONS")
add_item("\nMUST TRANSFER (Critical):")
add_item("  1. sentinel.db - Contains all trading data")
add_item("  2. config.py - Contains API keys (NEVER share publicly)")
add_item("  3. All .py files (will sync via OneDrive if in OneDrive folder)")
add_item("")
add_item("SHOULD TRANSFER:")
add_item("  4. requirements.txt - List of Python packages to reinstall")
add_item("  5. Documentation_Dev/ - All your guides and notes")
add_item("  6. Backups/ - Database backups")
add_item("")
add_item("NO NEED TO TRANSFER:")
add_item("  - venv/ folder - Recreate on new laptop")
add_item("  - __pycache__/ folders - Python regenerates these")
add_item("  - .git/ folder - Will sync from GitHub")

# Write report
report_file = sentinel_root / "Transfer_Inventory_Report.txt"
print(f"\n[8] Writing report to: {report_file}")

with open(report_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

print("\n" + "=" * 80)
print("INVENTORY COMPLETE")
print("=" * 80)
print(f"\nReport saved to: {report_file}")
print("\nNext steps:")
print("  1. Review the report")
print("  2. Run Create_Transfer_Package.py to backup critical files")
print("  3. Keep report and backup for new laptop setup")
print("\n" + "=" * 80 + "\n")
