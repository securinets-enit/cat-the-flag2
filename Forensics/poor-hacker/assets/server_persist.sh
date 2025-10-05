sudo tee /etc/systemd/system/flagserver.service > /dev/null <<'EOF'
[Unit]
Description=CTF Flag Server (Flask)
After=network.target

[Service]
Type=simple
User=salamnki
Group=salamnki
WorkingDirectory=/home/salamnki
# Use the venv python to run the script
ExecStart=/home/salamnki/venv/bin/python /home/salamnki/flag_server.py
Restart=always
RestartSec=3
# Limits (optional but helpful)
LimitNOFILE=4096

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now flagserver.service
sudo systemctl status flagserver.service --no-pager
sudo journalctl -u flagserver.service -f

