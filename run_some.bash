#!/bin/bash
ulimit -m 2048000
git pull && python3 utils/scripts/update_data.py
