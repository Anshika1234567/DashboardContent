// Chart.js configuration and utility functions

// Chart.js default configuration
Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = '#6c757d';

// Color palette for charts
const chartColors = {
    primary: '#007bff',
    success: '#28a745',
    warning: '#ffc107',
    danger: '#dc3545',
    info: '#17a2b8',
    light: '#f8f9fa',
    dark: '#343a40',
    secondary: '#6c757d'
};

// Gradient colors
const gradientColors = {
    primary: 'rgba(0, 123, 255, 0.1)',
    success: 'rgba(40, 167, 69, 0.1)',
    warning: 'rgba(255, 193, 7, 0.1)',
    danger: 'rgba(220, 53, 69, 0.1)',
    info: 'rgba(23, 162, 184, 0.1)'
};

// Common chart options
const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: true,
            position: 'bottom',
            labels: {
                usePointStyle: true,
                padding: 20,
                font: {
                    size: 12,
                    weight: '500'
                }
            }
        },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: '#fff',
            bodyColor: '#fff',
            borderColor: '#fff',
            borderWidth: 1,
            cornerRadius: 8,
            displayColors: true,
            callbacks: {
                title: function(context) {
                    return context[0].label;
                },
                label: function(context) {
                    return context.dataset.label + ': ' + context.parsed.y;
                }
            }
        }
    },
    scales: {
        x: {
            grid: {
                display: false
            },
            ticks: {
                font: {
                    size: 11
                }
            }
        },
        y: {
            grid: {
                color: 'rgba(0, 0, 0, 0.1)',
                drawBorder: false
            },
            ticks: {
                font: {
                    size: 11
                }
            }
        }
    }
};

// Create attendance pie chart
function createAttendancePieChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    return new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: [
                    chartColors.success,
                    chartColors.danger,
                    chartColors.warning
                ],
                borderColor: '#fff',
                borderWidth: 3,
                hoverOffset: 10
            }]
        },
        options: {
            ...commonOptions,
            plugins: {
                ...commonOptions.plugins,
                legend: {
                    ...commonOptions.plugins.legend,
                    position: 'right'
                }
            }
        }
    });
}

// Create attendance trends chart
function createAttendanceTrendsChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Create gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(0, 123, 255, 0.3)');
    gradient.addColorStop(1, 'rgba(0, 123, 255, 0.05)');
    
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Attendance %',
                data: data.values,
                borderColor: chartColors.primary,
                backgroundColor: gradient,
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: chartColors.primary,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    min: 0,
                    max: 100,
                    ticks: {
                        ...commonOptions.scales.y.ticks,
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

// Create monthly trends bar chart
function createMonthlyTrendsChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Present Days',
                data: data.values,
                backgroundColor: chartColors.primary,
                borderColor: chartColors.primary,
                borderWidth: 1,
                borderRadius: 4,
                borderSkipped: false
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    beginAtZero: true,
                    ticks: {
                        ...commonOptions.scales.y.ticks,
                        stepSize: 1
                    }
                }
            }
        }
    });
}

// Create weekly attendance chart
function createWeeklyAttendanceChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Present Days',
                data: data.values,
                backgroundColor: [
                    chartColors.success,
                    chartColors.warning,
                    chartColors.danger,
                    chartColors.info,
                    chartColors.primary,
                    chartColors.secondary,
                    chartColors.success
                ],
                borderColor: '#fff',
                borderWidth: 2,
                borderRadius: 6
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    beginAtZero: true,
                    max: 7,
                    ticks: {
                        ...commonOptions.scales.y.ticks,
                        stepSize: 1
                    }
                }
            }
        }
    });
}

// Create attendance comparison chart
function createAttendanceComparisonChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    return new Chart(ctx, {
        type: 'radar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Student Attendance',
                data: data.values,
                borderColor: chartColors.primary,
                backgroundColor: 'rgba(0, 123, 255, 0.2)',
                borderWidth: 2,
                pointBackgroundColor: chartColors.primary,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom'
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    min: 0,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

// Utility function to format date labels
function formatDateLabels(dates) {
    return dates.map(date => {
        const d = new Date(date);
        return d.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric' 
        });
    });
}

// Utility function to format month labels
function formatMonthLabels(months) {
    return months.map(month => {
        const [year, monthNum] = month.split('-');
        const date = new Date(year, monthNum - 1);
        return date.toLocaleDateString('en-US', { 
            month: 'short', 
            year: '2-digit' 
        });
    });
}

// Utility function to get attendance status color
function getAttendanceStatusColor(percentage) {
    if (percentage >= 90) return chartColors.success;
    if (percentage >= 75) return chartColors.warning;
    return chartColors.danger;
}

// Utility function to animate counter
function animateCounter(element, start, end, duration) {
    const startTime = performance.now();
    const isNumber = !isNaN(start) && !isNaN(end);
    
    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = start + (end - start) * progress;
        element.textContent = isNumber ? Math.round(current) : current;
        
        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        }
    }
    
    requestAnimationFrame(updateCounter);
}

// Export functions for global use
window.ChartUtils = {
    createAttendancePieChart,
    createAttendanceTrendsChart,
    createMonthlyTrendsChart,
    createWeeklyAttendanceChart,
    createAttendanceComparisonChart,
    formatDateLabels,
    formatMonthLabels,
    getAttendanceStatusColor,
    animateCounter,
    chartColors,
    commonOptions
};



