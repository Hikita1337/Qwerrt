#!/bin/bash

echo "Installing deps…"
pip install -r requirements.txt

echo "Starting mitmdump…"
mkdir -p dumps

mitmdump --listen-host 0.0.0.0 --listen-port 8080 -s mitm_addons/mitm_logger.py