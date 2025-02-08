from flask import Flask, render_template
import psutil
from datetime import datetime

app = Flask(__name__)

# Custom filter to convert timestamp to date
@app.template_filter('timestamp_to_date')
def timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    # Get system stats
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    boot_time = psutil.boot_time()
    network_info = psutil.net_io_counters()

    # Convert stats to human-readable format
    stats = {
        'cpu_usage': cpu_usage,
        'memory_used': memory_info.used // (1024 ** 2),  # in MB
        'memory_total': memory_info.total // (1024 ** 2),  # in MB
        'disk_used': disk_usage.used // (1024 ** 3),  # in GB
        'disk_total': disk_usage.total // (1024 ** 3),  # in GB
        'boot_time': boot_time,
        'network_sent': network_info.bytes_sent // (1024 ** 2),  # in MB
        'network_recv': network_info.bytes_recv // (1024 ** 2),  # in MB
    }

    return render_template('index.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True)