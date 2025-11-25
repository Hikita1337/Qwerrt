#!/bin/bash
mkdir -p dumps/files
mkdir -p dumps/ws
mkdir -p dumps/requests
mkdir -p dumps/responses

mitmweb \
  --listen-host 0.0.0.0 \
  --listen-port 8080 \
  --web-host 0.0.0.0 \
  --web-port 8081 \
  -s mitm_addons/mitm_logger.py