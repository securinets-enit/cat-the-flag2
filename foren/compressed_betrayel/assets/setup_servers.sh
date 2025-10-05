[Unit]
Description=CTF Server 1
After=network.target

[Service]
WorkingDirectory=/home/compression/server-setup/main/server1
ExecStart=/usr/bin/python3 -m http.server 2982
Restart=always
User=compression

[Install]
WantedBy=multi-user.target

