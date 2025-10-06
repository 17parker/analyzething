#!/bin/bash
# run_tests.sh - Run all the pytest tests for Large Graph Path Finder
# Usage: ./run_tests.sh
set -e
cd "$(dirname "$0")"
# this run_test.sh already at root
pytest -v