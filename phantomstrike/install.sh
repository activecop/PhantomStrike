# Install dependencies
sudo apt update
sudo apt install python3-scapy python3-cryptography aircrack-ng arp-scan nmap mdk3 mdk4 -y

# Copy to system
sudo mkdir -p /opt/phantomstrike
sudo cp phantomstrike.py /opt/phantomstrike/
sudo chmod +x /opt/phantomstrike/phantomstrike.py

# Create shortcut
sudo bash -c 'cat > /usr/local/bin/phantomstrike << EOF
#!/bin/bash
python3 /opt/phantomstrike/phantomstrike.py "\$@"
EOF'
sudo chmod +x /usr/local/bin/phantomstrike