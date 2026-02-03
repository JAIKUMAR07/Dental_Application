"""
Simple script to restart and run the backend with proper logging
"""
import subprocess
import sys
import time

print("🔄 Restarting backend server...")
print("=" * 60)

# Kill any existing Python processes on port 8000
try:
    subprocess.run(
        ["powershell", "-Command", "Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }"],
        timeout=5
    )
    print("✅ Stopped existing server")
    time.sleep(2)
except:
    print("ℹ️  No existing server found")

# Start the server
print("\n🚀 Starting FastAPI server...")
print("=" * 60)
print()

try:
    subprocess.run(
        [sys.executable, "main.py"],
        cwd="app"
    )
except KeyboardInterrupt:
    print("\n\n👋 Server stopped")
