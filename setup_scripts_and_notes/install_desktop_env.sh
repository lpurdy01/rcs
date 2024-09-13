#!/bin/bash
# Update package lists and upgrade existing packages
sudo apt update && sudo apt upgrade -y

# Install the Xfce desktop environment
sudo apt install -y xfce4 xfce4-goodies

# Install xrdp for remote desktop protocol
sudo apt install -y xrdp

# Enable and start the xrdp service
sudo systemctl enable xrdp && sudo systemctl start xrdp

# Add xrdp user to the ssl-cert group
sudo adduser xrdp ssl-cert

# Allow RDP through the firewall
sudo ufw allow 3389/tcp

# Restart xrdp service to apply changes
sudo systemctl restart xrdp
