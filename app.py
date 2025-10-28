from flask import Flask, render_template, request, jsonify
from database import db
import json
from datetime import datetime, date

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Main dashboard view"""
    return render_template('dashboard.html')

@app.route('/api/stats/<student_name>')
def get_student_stats(student_name):
    """Get individual student statistics"""
    try:
        stats = db.get_student_stats(student_name)
        if not stats:
            return jsonify({'error': 'Student not found'}), 404
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/all')
def get_all_stats():
    """Get statistics for all students"""
    try:
        all_stats = db.get_all_students_stats()
        class_average = db.get_class_average_attendance()
        return jsonify({
            'students': all_stats,
            'class_average': class_average
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance/manual', methods=['POST'])
def manual_attendance():
    """Manual attendance entry"""
    try:
        data = request.get_json()
        student_name = data.get('student_name')
        status = data.get('status', 'present')
        entry_type = 'manual'
        
        if not student_name:
            return jsonify({'error': 'Student name is required'}), 400
        
        success = db.log_attendance(student_name, status, entry_type)
        if success:
            return jsonify({'message': 'Attendance logged successfully'})
        else:
            return jsonify({'error': 'Failed to log attendance or already logged today'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance/history')
def get_attendance_history():
    """Get attendance history with optional filters"""
    try:
        student_name = request.args.get('student_name')
        days = int(request.args.get('days', 30))
        
        history = db.get_attendance_history(student_name, days)
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students')
def get_students():
    """Get list of all students"""
    try:
        conn = db.db_path
        import sqlite3
        conn = sqlite3.connect(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM students ORDER BY name")
        students = [row[0] for row in cursor.fetchall()]
        conn.close()
        return jsonify(students)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance/trends/<student_name>')
def get_attendance_trends(student_name):
    """Get attendance trends data for charts"""
    try:
        stats = db.get_student_stats(student_name)
        if not stats:
            return jsonify({'error': 'Student not found'}), 404
        
        # Format data for Chart.js
        trends_data = {
            'monthly': {
                'labels': [item[0] for item in stats['monthly_data']],
                'datasets': [{
                    'label': 'Present Days',
                    'data': [item[2] for item in stats['monthly_data']],
                    'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'borderWidth': 1
                }]
            },
            'weekly': {
                'labels': [item[0] for item in stats['weekly_data']],
                'datasets': [{
                    'label': 'Present Days',
                    'data': [item[2] for item in stats['weekly_data']],
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'borderColor': 'rgba(75, 192, 192, 1)',
                    'borderWidth': 1
                }]
            }
        }
        
        return jsonify(trends_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance/summary')
def get_attendance_summary():
    """Get overall attendance summary for the dashboard"""
    try:
        all_stats = db.get_all_students_stats()
        class_average = db.get_class_average_attendance()
        
        # Calculate summary statistics
        total_students = len(all_stats)
        total_present_days = sum(stats['present_days'] for stats in all_stats)
        total_days = sum(stats['total_days'] for stats in all_stats)
        overall_percentage = (total_present_days / total_days * 100) if total_days > 0 else 0
        
        # Get today's attendance
        today = date.today()
        today_attendance = []
        for stats in all_stats:
            student_name = stats['student_name']
            # Check if student was present today and get last marked time
            history = db.get_attendance_history(student_name, 1)
            present_today = False
            last_marked_time = None
            
            for record in history:
                if record['timestamp'].startswith(today.strftime('%Y-%m-%d')):
                    present_today = record['status'] == 'present'
                    last_marked_time = record['timestamp']
                    break
            
            today_attendance.append({
                'student_name': student_name,
                'present': present_today,
                'last_marked_time': last_marked_time
            })
        
        summary = {
            'total_students': total_students,
            'total_present_days': total_present_days,
            'total_days': total_days,
            'overall_percentage': round(overall_percentage, 2),
            'class_average': class_average,
            'today_attendance': today_attendance
        }
        
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

