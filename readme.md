# Flask Task Manager

A simple Flask app to display system stats like CPU usage, memory usage, disk usage, and more.

## Features
- Real-time system stats
- Responsive and colorful UI
- Easy to deploy

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/task-manager.git

2. Navigate to the project folder:
    cd flask-task-manager

3. Set up virtual enviroment and install dependencies: 
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

4. Run the app:
    python app.py

# **Deploying a Flask Application with Gunicorn and Nginx** 
- This guide explains how to deploy a Flask application using **Gunicorn** as the WSGI server and **Nginx** as a reverse proxy.

## **1. Install Dependencies**  

- Ensure your system has the necessary packages installed:

```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

- Navigate to your Flask project directory:
```bash
cd /path/to/your/project
```

- Create and activate a virtual environment and install dependencies: 
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## **2. Test Flask App Locally**
- Before deploying, test if the app runs correctly:
```bash
python app.py
```
- Your Flask app should be accessible at http://127.0.0.1:5000.

## **3. Set Up Gunicorn**
- Install Gunicorn and then test it:
```bash
pip install gunicorn
gunicorn --bind 127.0.0.1:8000 wsgi:app
```

- To run Gunicorn in the background, create a systemd service:
```bash
sudo nano /etc/systemd/system/your_project.service
```
- Add the following:
```bash
[Unit]
Description=Gunicorn instance to serve Flask Application
After=network.target

[Service]
User=your_user
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/project/venv/bin/gunicorn --workers 3 --bind unix:/path/to/your/project/your_project.sock wsgi:app

[Install]
WantedBy=multi-user.target
```
- Enable and start Gunicorn:
```bash
sudo systemctl daemon-reload
sudo systemctl enable your_project
sudo systemctl start your_project
```
- Check if it's running:
```bash
sudo systemctl status your_project
```

## **4. Configure Nginx**
- Create an Nginx configuration file:
```bash
sudo nano /etc/nginx/sites-available/your_project
```
- Add the following:
```bash
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://unix:/path/to/your/project/your_project.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/project/static/;
    }
}
```
- Enable the configuration:
```bash
sudo ln -s /etc/nginx/sites-available/your_project /etc/nginx/sites-enabled/
```
- Test and restart Nginx:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

## **5. Ensure Proper File Permissions **
- Make sure Nginx can access the project files:
```bash
sudo chown -R www-data:www-data /path/to/your/project
sudo chmod -R 755 /path/to/your/project
```

## **6. Restarting and checking Services**
- If you need to restart aplication:
```bash
sudo systemctl restart your_project
sudo systemctl restart nginx
```
- To check service status:
```bash
sudo systemctl status your_project
sudo systemctl status nginx
```

## **7. Accessing the Application**
- http://your_server_ip
- http://localhost/