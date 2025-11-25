#!/bin/bash

echo "Installing mitmproxy…"
pip install mitmproxy

echo "Starting mitmdump (no GUI)…"
mkdir -p dumps

mitmdump --listen-host 0.0.0.0 --listen-port 8080 -s mitm_addons/mitm_logger.py