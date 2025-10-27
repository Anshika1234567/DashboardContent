#!/usr/bin/env python3
"""
Test script to demonstrate time display functionality
This script adds some sample attendance records with different times
"""

from database import db
from datetime import datetime, timedelta
import random

def add_sample_attendance():
    """Add sample attendance records with different times"""
    
    # Get all students
    conn = db.db_path
    import sqlite3
    conn = sqlite3.connect(conn)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM students")
    students = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    if not students:
        print("No students found. Please run main.py first to initialize students.")
        return
    
    print(f"Found {len(students)} students: {', '.join(students)}")
    
    # Add some sample attendance for today with different times
    today = datetime.now().date()
    
    # Sample times throughout the day
    sample_times = [
        "08:30:00",  # Early morning
        "09:15:00",  # Regular time
        "09:45:00",  # Late arrival
        "10:30:00",  # Very late
        "11:00:00"   # Very late
    ]
    
    print("\nAdding sample attendance records...")
    
    for i, student in enumerate(students):
        # Clear existing attendance for today first
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM attendance 
            WHERE student_id = (SELECT id FROM students WHERE name = ?) 
            AND DATE(timestamp) = ?
        """, (student, today))
        conn.commit()
        conn.close()
        
        # Add new attendance record
        time_str = sample_times[i % len(sample_times)]
        timestamp = f"{today} {time_str}"
        
        # Create a custom timestamp for testing
        success = db.log_attendance(student, 'present', 'automatic')
        
        if success:
            # Update the timestamp to our sample time
            conn = sqlite3.connect(db.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE attendance 
                SET timestamp = ? 
                WHERE student_id = (SELECT id FROM students WHERE name = ?) 
                AND DATE(timestamp) = ?
                ORDER BY timestamp DESC 
                LIMIT 1
            """, (timestamp, student, today))
            conn.commit()
            conn.close()
            
            print(f"✅ {student}: {time_str} AM/PM")
        else:
            print(f"❌ Failed to add attendance for {student}")
    
    print("\n🎉 Sample attendance records added!")
    print("📊 Check the dashboard at http://localhost:5000 to see the time display")
    print("🕐 Times are displayed in 12-hour format (AM/PM)")

if __name__ == "__main__":
    add_sample_attendance()



