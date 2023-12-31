#!/usr/bin/env bash
# This script sets up web servers for deployment of web traffic

# Check if Nginx is installed, install if not
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get -y upgrade
    sudo apt-get install -y nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared
sudo touch /data/web_static/releases/test/index.html

# Add content to the test HTML file
echo "<html><head><title>Test Page</title></head><body>This is a test page.</body></html>" | sudo tee /data/web_static/releases/test/index.html >/dev/null

# Remove existing symbolic link and create a new one
sudo rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership of directories to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to add missing location block
nginx_config="/etc/nginx/sites-available/default"

# Check if location block for /hbnb_static/ already exists, if not, add it
if ! grep -q "location \/hbnb_static\/ {" "$nginx_config"; then
    sudo sed -i '/server_name _;/a \\n\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t}\n' "$nginx_config"
fi

# Restart Nginx
sudo service nginx restart
