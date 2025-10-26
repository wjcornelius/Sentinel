#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configuration Setup Helper for Sentinel

This script helps you create a config.py file from the template
or validates an existing configuration.
"""

import os
import sys


def check_config_exists():
    """Check if config.py exists."""
    return os.path.exists("config.py")


def check_config_template_exists():
    """Check if config.example.py exists."""
    return os.path.exists("config.example.py")


def create_config_from_template():
    """Copy config.example.py to config.py."""
    if not check_config_template_exists():
        print("[ERROR] config.example.py not found!")
        return False

    if check_config_exists():
        response = input("config.py already exists. Overwrite? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Cancelled.")
            return False

    try:
        with open("config.example.py", "r") as template:
            content = template.read()

        with open("config.py", "w") as config:
            config.write(content)

        print("[SUCCESS] Created config.py from template")
        print("\nNext steps:")
        print("1. Open config.py in your text editor")
        print("2. Replace all placeholder values with your actual API keys")
        print("3. Save the file")
        print("4. Run this script again with --validate to check your config")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to create config.py: {e}")
        return False


def validate_config():
    """Validate that config.py has real values (not placeholders)."""
    if not check_config_exists():
        print("[ERROR] config.py not found!")
        print("Run: python setup_config.py --create")
        return False

    try:
        import config

        placeholders_found = []
        required_keys = [
            'APCA_API_KEY_ID',
            'APCA_API_SECRET_KEY',
            'OPENAI_API_KEY',
            'PERPLEXITY_API_KEY'
        ]

        print("Validating configuration...\n")

        for key in required_keys:
            value = getattr(config, key, None)
            if value is None:
                print(f"[MISSING] {key}")
                placeholders_found.append(key)
            elif "YOUR_" in value or "HERE" in value:
                print(f"[PLACEHOLDER] {key} = {value}")
                placeholders_found.append(key)
            else:
                # Mask the actual key for security
                masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
                print(f"[OK] {key} = {masked}")

        print(f"\n[INFO] LIVE_TRADING = {config.LIVE_TRADING}")
        print(f"[INFO] ALLOW_DEV_RERUNS = {getattr(config, 'ALLOW_DEV_RERUNS', False)}")

        if placeholders_found:
            print(f"\n[WARNING] {len(placeholders_found)} placeholder(s) found")
            print("Please edit config.py and replace placeholder values with real API keys")
            return False
        else:
            print("\n[SUCCESS] All required configuration keys are set!")
            return True

    except ImportError as e:
        print(f"[ERROR] Could not import config.py: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Validation failed: {e}")
        return False


def main():
    """Main entry point."""
    print("=" * 60)
    print("Sentinel Configuration Setup Helper")
    print("=" * 60)
    print()

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "--create":
            create_config_from_template()
        elif command == "--validate":
            validate_config()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python setup_config.py [--create|--validate]")
    else:
        # Interactive mode
        if check_config_exists():
            print("config.py exists. What would you like to do?")
            print("  1. Validate existing configuration")
            print("  2. Create new config from template (overwrites existing)")
            print("  3. Exit")
            choice = input("\nEnter choice (1/2/3): ").strip()

            if choice == "1":
                validate_config()
            elif choice == "2":
                create_config_from_template()
            else:
                print("Exiting.")
        else:
            print("config.py not found.")
            response = input("Create config.py from template? (yes/no): ")
            if response.lower() in ['yes', 'y']:
                create_config_from_template()

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
