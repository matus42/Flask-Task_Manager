from flask import Flask, render_template, jsonify
import psutil
import platform
from datetime import datetime

app = Flask(__name__, static_folder="static")

@app.route('/data')
def get_data():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    boot_time = psutil.boot_time()
    network_info = psutil.net_io_counters()

    data = {
        'cpu_usage': cpu_usage,
        'memory_used': memory_info.used // (1024 ** 2),
        'memory_total': memory_info.total // (1024 ** 2),
        'disk_used': disk_usage.used // (1024 ** 3),
        'disk_total': disk_usage.total // (1024 ** 3),
        'boot_time': datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S'), # Format boot time here
        'network_sent': network_info.bytes_sent // (1024 ** 2),
        'network_recv': network_info.bytes_recv // (1024 ** 2),
    }
    return jsonify(data)  # Return data as JSON

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

@app.route('/processes')
def processes():
    # Get running processes
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        processes.append(proc.info)
    return render_template('processes.html', processes=processes)

@app.route('/system-info')
def system_info():
    # Get system information
    system_info = {
        'os': platform.system(),
        'os_version': platform.version(),
        'python_version': platform.python_version(),
        'hostname': platform.node(),
        'processor': platform.processor(),
    }
    return render_template('system_info.html', system_info=system_info)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/processes_data')
def get_processes_data():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        processes.append(proc.info)
    return jsonify(processes)

@app.route('/system_info_data')
def get_system_info_data():
    system_info = {
        'os': platform.system(),
        'os_version': platform.version(),
        'python_version': platform.python_version(),
        'hostname': platform.node(),
        'processor': platform.processor(),
    }
    return jsonify(system_info)