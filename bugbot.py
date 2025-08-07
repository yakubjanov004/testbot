#!/usr/bin/env python3
"""
BugBot - Alfa Connect Bot Runner

This script provides the 'bugbot' command interface for running the Alfa Connect bot.
"""

import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """Check and install required dependencies"""
    try:
        import aiogram
        import dotenv
        return True
    except ImportError as e:
        print(f"⚠️ Missing dependency: {e}")
        print("📦 Installing dependencies...")
        
        # Try to install using pip
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", 
                                 "--break-system-packages",
                                 "aiogram>=3.0.0", "python-dotenv>=0.19.0"])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies automatically")
            print("💡 Please install manually:")
            print("   pip install --break-system-packages aiogram python-dotenv")
            return False

def main():
    """Main function for bugbot command"""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Check if main.py exists
    main_py = script_dir / "main.py"
    if not main_py.exists():
        print("❌ Error: main.py not found!")
        print(f"📁 Current directory: {script_dir}")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Get command line arguments
    args = sys.argv[1:] if len(sys.argv) > 1 else ['run']
    
    # Build the command
    cmd = [sys.executable, str(main_py)] + args
    
    try:
        print("🚀 Starting BugBot...")
        print(f"📁 Working directory: {script_dir}")
        print(f"🔧 Command: {' '.join(cmd)}")
        print("-" * 50)
        
        # Run the bot
        result = subprocess.run(cmd, cwd=script_dir)
        
        if result.returncode == 0:
            print("-" * 50)
            print("✅ BugBot stopped successfully")
        else:
            print("-" * 50)
            print(f"❌ BugBot stopped with error code: {result.returncode}")
            sys.exit(result.returncode)
            
    except KeyboardInterrupt:
        print("\n⏹️ BugBot stopped by user")
    except Exception as e:
        print(f"❌ Error running BugBot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()