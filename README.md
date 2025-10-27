# Student Attendance Dashboard with Face Recognition

A comprehensive attendance tracking system that combines face recognition technology with a modern web dashboard for monitoring student attendance statistics.

## Features

### 🎯 Core Features
- **Face Recognition**: Automatic attendance logging using DeepFace
- **Web Dashboard**: Modern, responsive web interface
- **Real-time Statistics**: Live attendance tracking and analytics
- **Manual Entry**: Option to manually log attendance
- **Comprehensive Reports**: Detailed attendance analytics and trends

### 📊 Dashboard Statistics
- Overall attendance percentage
- Individual student statistics
- Monthly and weekly trends
- Attendance streaks
- Late arrival tracking
- Class average comparison
- Today's attendance status

### 🎨 User Interface
- Modern Bootstrap 5 design
- Interactive charts using Chart.js
- Responsive mobile-friendly layout
- Real-time data updates
- Toast notifications

## Installation

### Prerequisites
- Python 3.8 or higher
- Webcam for face recognition
- Modern web browser

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd face_recog
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add student photos**
   - Place student photos in the `known_faces/` folder
   - Name files as `StudentName.jpg` (e.g., `JohnDoe.jpg`)
   - Supported formats: JPG, PNG, JPEG

4. **Initialize the database**
   - The database will be created automatically on first run
   - Students will be registered automatically from photos

## Usage

### Starting the System

1. **Start the Dashboard Server**
   ```bash
   python run_dashboard.py
   ```
   - Dashboard will be available at: http://localhost:5000

2. **Start Face Recognition (in another terminal)**
   ```bash
   python main.py
   ```
   - Webcam will open for face recognition
   - Attendance will be logged automatically when faces are recognized

### Using the Dashboard

1. **View Statistics**
   - Open http://localhost:5000 in your browser
   - View overall attendance statistics
   - Check individual student performance

2. **Manual Entry**
   - Click "Manual Entry" button
   - Select student and status
   - Submit to log attendance

3. **Student Details**
   - Click the eye icon next to any student
   - View detailed statistics and recent attendance

## File Structure

```
face_recog/
├── main.py                 # Face recognition system
├── database.py             # Database models and queries
├── run_dashboard.py        # Dashboard server runner
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── known_faces/           # Student photos
│   ├── Anshika.jpg
│   ├── nida.jpg
│   ├── Saima.jpg
│   └── Sehreen.jpg
├── DashBoard/
│   ├── app.py             # Flask application
│   ├── templates/
│   │   └── dashboard.html # Main dashboard UI
│   └── static/
│       ├── css/
│       │   └── style.css  # Custom styles
│       └── js/
│           └── charts.js  # Chart utilities
└── attendance.db          # SQLite database (created automatically)
```

## API Endpoints

### Dashboard Routes
- `GET /` - Main dashboard
- `GET /api/stats/all` - All students statistics
- `GET /api/stats/<student_name>` - Individual student stats
- `GET /api/attendance/summary` - Overall attendance summary
- `GET /api/attendance/history` - Attendance history
- `POST /api/attendance/manual` - Manual attendance entry
- `GET /api/students` - List all students

## Database Schema

### Students Table
- `id` - Primary key
- `name` - Student name
- `photo_filename` - Photo file name
- `enrollment_date` - Date added to system

### Attendance Table
- `id` - Primary key
- `student_id` - Foreign key to students
- `timestamp` - When attendance was logged
- `status` - present/absent/late
- `entry_type` - automatic/manual

## Configuration

### Face Recognition Settings
- **Model**: Facenet512
- **Threshold**: 0.3 (adjustable in main.py)
- **Check Interval**: 3 seconds

### Dashboard Settings
- **Port**: 5000
- **Host**: 0.0.0.0 (accessible from network)
- **Debug Mode**: Enabled

## Troubleshooting

### Common Issues

1. **Face Recognition Not Working**
   - Ensure webcam is connected and working
   - Check if student photos are in correct format
   - Verify DeepFace installation

2. **Dashboard Not Loading**
   - Check if port 5000 is available
   - Verify Flask installation
   - Check console for error messages

3. **Database Errors**
   - Ensure write permissions in project directory
   - Check if SQLite is properly installed

### Performance Tips

1. **Face Recognition**
   - Use good lighting for better recognition
   - Ensure student photos are clear and front-facing
   - Adjust threshold if needed (lower = more sensitive)

2. **Dashboard**
   - Refresh data periodically for real-time updates
   - Use manual entry for backup logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the console output for errors
3. Ensure all dependencies are installed correctly

---

**Note**: This system is designed for educational purposes. Ensure compliance with privacy laws and regulations when using face recognition technology.



