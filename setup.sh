#!/bin/bash

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add project root to PYTHONPATH
echo 'export PYTHONPATH="$PYTHONPATH:$(pwd)"' >> venv/bin/activate
