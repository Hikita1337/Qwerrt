#!/bin/bash

# Запускаем mitmdump на 0.0.0.0:8080
nohup mitmdump --listen-host 0.0.0.0 -p 8080 --set block_global=false --scripts mitm_addons/mitm_logger.py >mitm.log 2>&1 &

sleep 2

echo "MITMProxy запущен на 0.0.0.0:8080"
echo "Запускаю Cloudflared TCP туннель..."

# Запускаем cloudflared tcp туннель на порт 8080
cloudflared tunnel --url tcp://localhost:8080