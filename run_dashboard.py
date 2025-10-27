#!/usr/bin/env python3
"""
Student Attendance Dashboard Runner
This script starts the Flask dashboard server for the attendance system.
"""

import os
import sys
from DashBoard.app import app

def main():
    """Main function to run the dashboard"""
    print("🎓 Starting Student Attendance Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("📷 Face recognition system: Run 'python main.py' in another terminal")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Run the Flask app
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=False  # Disable reloader to avoid conflicts
        )
    except KeyboardInterrupt:
        print("\n🛑 Dashboard server stopped.")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
