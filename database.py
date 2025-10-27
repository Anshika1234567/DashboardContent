import sqlite3
import os
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple

class AttendanceDB:
    def __init__(self, db_path: str = "attendance.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                photo_filename TEXT,
                enrollment_date DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        # Create attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'present',
                entry_type TEXT DEFAULT 'automatic',
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_student(self, name: str, photo_filename: str = None) -> int:
        """Add a new student to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO students (name, photo_filename) VALUES (?, ?)",
                (name, photo_filename)
            )
            student_id = cursor.lastrowid
            conn.commit()
            return student_id
        except sqlite3.IntegrityError:
            # Student already exists, get their ID
            cursor.execute("SELECT id FROM students WHERE name = ?", (name,))
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            conn.close()
    
    def log_attendance(self, student_name: str, status: str = 'present', entry_type: str = 'automatic') -> bool:
        """Log attendance for a student"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get or create student
            student_id = self.add_student(student_name)
            if not student_id:
                return False
            
            # Check if already logged today
            today = date.today()
            cursor.execute('''
                SELECT id FROM attendance 
                WHERE student_id = ? AND DATE(timestamp) = ? AND entry_type = ?
            ''', (student_id, today, entry_type))
            
            if cursor.fetchone():
                print(f"Attendance already logged for {student_name} today")
                return False
            
            # Log attendance
            cursor.execute('''
                INSERT INTO attendance (student_id, status, entry_type) 
                VALUES (?, ?, ?)
            ''', (student_id, status, entry_type))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error logging attendance: {e}")
            return False
        finally:
            conn.close()
    
    def get_student_stats(self, student_name: str) -> Dict:
        """Get comprehensive statistics for a student"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get student ID
            cursor.execute("SELECT id FROM students WHERE name = ?", (student_name,))
            result = cursor.fetchone()
            if not result:
                return {}
            
            student_id = result[0]
            
            # Get total attendance count
            cursor.execute('''
                SELECT COUNT(*) FROM attendance 
                WHERE student_id = ? AND status = 'present'
            ''', (student_id,))
            present_days = cursor.fetchone()[0]
            
            # Get total days in database
            cursor.execute('''
                SELECT COUNT(DISTINCT DATE(timestamp)) FROM attendance 
                WHERE student_id = ?
            ''', (student_id,))
            total_days = cursor.fetchone()[0]
            
            # Get attendance percentage
            attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
            
            # Get recent attendance (last 30 days)
            cursor.execute('''
                SELECT DATE(timestamp), status FROM attendance 
                WHERE student_id = ? AND timestamp >= datetime('now', '-30 days')
                ORDER BY timestamp DESC
            ''', (student_id,))
            recent_attendance = cursor.fetchall()
            
            # Get monthly breakdown
            cursor.execute('''
                SELECT strftime('%Y-%m', timestamp) as month, 
                       COUNT(*) as days,
                       SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present
                FROM attendance 
                WHERE student_id = ?
                GROUP BY strftime('%Y-%m', timestamp)
                ORDER BY month DESC
            ''', (student_id,))
            monthly_data = cursor.fetchall()
            
            # Get weekly data (last 12 weeks)
            cursor.execute('''
                SELECT strftime('%Y-W%W', timestamp) as week,
                       COUNT(*) as days,
                       SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present
                FROM attendance 
                WHERE student_id = ? AND timestamp >= datetime('now', '-84 days')
                GROUP BY strftime('%Y-W%W', timestamp)
                ORDER BY week DESC
            ''', (student_id,))
            weekly_data = cursor.fetchall()
            
            # Get attendance streak
            cursor.execute('''
                SELECT DATE(timestamp), status FROM attendance 
                WHERE student_id = ?
                ORDER BY timestamp DESC
            ''', (student_id,))
            all_attendance = cursor.fetchall()
            
            current_streak = 0
            for record in all_attendance:
                if record[1] == 'present':
                    current_streak += 1
                else:
                    break
            
            # Get late arrivals (after 9 AM)
            cursor.execute('''
                SELECT COUNT(*) FROM attendance 
                WHERE student_id = ? AND status = 'present' 
                AND strftime('%H', timestamp) > '09'
            ''', (student_id,))
            late_arrivals = cursor.fetchone()[0]
            
            return {
                'student_name': student_name,
                'present_days': present_days,
                'total_days': total_days,
                'attendance_percentage': round(attendance_percentage, 2),
                'recent_attendance': recent_attendance,
                'monthly_data': monthly_data,
                'weekly_data': weekly_data,
                'current_streak': current_streak,
                'late_arrivals': late_arrivals
            }
        except Exception as e:
            print(f"Error getting student stats: {e}")
            return {}
        finally:
            conn.close()
    
    def get_all_students_stats(self) -> List[Dict]:
        """Get statistics for all students"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT name FROM students")
            students = cursor.fetchall()
            
            all_stats = []
            for student in students:
                stats = self.get_student_stats(student[0])
                if stats:
                    all_stats.append(stats)
            
            return all_stats
        except Exception as e:
            print(f"Error getting all students stats: {e}")
            return []
        finally:
            conn.close()
    
    def get_attendance_history(self, student_name: str = None, days: int = 30) -> List[Dict]:
        """Get attendance history with optional filters"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            if student_name:
                cursor.execute('''
                    SELECT s.name, a.timestamp, a.status, a.entry_type
                    FROM attendance a
                    JOIN students s ON a.student_id = s.id
                    WHERE s.name = ? AND a.timestamp >= datetime('now', '-{} days')
                    ORDER BY a.timestamp DESC
                '''.format(days), (student_name,))
            else:
                cursor.execute('''
                    SELECT s.name, a.timestamp, a.status, a.entry_type
                    FROM attendance a
                    JOIN students s ON a.student_id = s.id
                    WHERE a.timestamp >= datetime('now', '-{} days')
                    ORDER BY a.timestamp DESC
                '''.format(days))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'student_name': row[0],
                    'timestamp': row[1],
                    'status': row[2],
                    'entry_type': row[3]
                })
            
            return history
        except Exception as e:
            print(f"Error getting attendance history: {e}")
            return []
        finally:
            conn.close()
    
    def get_class_average_attendance(self) -> float:
        """Get average attendance percentage for all students"""
        all_stats = self.get_all_students_stats()
        if not all_stats:
            return 0
        
        total_percentage = sum(stats['attendance_percentage'] for stats in all_stats)
        return round(total_percentage / len(all_stats), 2)

# Initialize database instance
db = AttendanceDB()

