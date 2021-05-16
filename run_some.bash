#!/bin/bash
ulimit -m 2048000
git pull && python3 update_data_v2.py
