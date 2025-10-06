#!/bin/bash
# run.sh - Launch Large Graph Path Finder

set -e
cd "$(dirname "$0")"

# Always run from project root
python3 -m core.main
