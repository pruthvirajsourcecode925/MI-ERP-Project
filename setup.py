#!/usr/bin/env python3
"""
Complete setup script for Mauli Industries ERP System
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*50}")
    print(f"STEP: {description}")
    print(f"COMMAND: {command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ SUCCESS: {description}")
            if result.stdout:
                print(f"OUTPUT: {result.stdout}")
        else:
            print(f"❌ FAILED: {description}")
            print(f"ERROR: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ EXCEPTION: {description}")
        print(f"ERROR: {e}")
        return False
    
    return True

def main():
    """Main setup function."""
    print("🚀 Mauli Industries ERP System - Complete Setup")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("app/main.py"):
        print("❌ ERROR: Please run this script from the project root directory")
        sys.exit(1)
    
    steps = [
        ("python -m venv venv", "Creating Python virtual environment"),
        ("venv\\Scripts\\activate && pip install --upgrade pip", "Upgrading pip"),
        ("venv\\Scripts\\activate && pip install -r requirements.txt", "Installing Python dependencies"),
        ("venv\\Scripts\\activate && pip install email-validator bcrypt requests", "Installing additional dependencies"),
        ("venv\\Scripts\\activate && python init_db.py", "Initializing database and creating super admin"),
    ]
    
    failed_steps = []
    
    for command, description in steps:
        if not run_command(command, description):
            failed_steps.append(description)
    
    print(f"\n{'='*60}")
    print("SETUP SUMMARY")
    print(f"{'='*60}")
    
    if failed_steps:
        print(f"❌ SETUP FAILED - {len(failed_steps)} step(s) failed:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\nPlease fix the errors and run the setup again.")
        return False
    else:
        print("✅ SETUP COMPLETED SUCCESSFULLY!")
        print("\nNext steps:")
        print("1. Start the server: python run.py")
        print("2. Visit API docs: http://localhost:8000/docs")
        print("3. Test with: python test_api.py")
        print("\nDefault Super Admin:")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Email: admin@mauliindustries.com")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
