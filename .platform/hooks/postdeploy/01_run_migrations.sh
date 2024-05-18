#!/bin/bash

# Navigate to the application directory
cd /var/app/staging

# Activate the virtual environment
source /var/app/venv/*/bin/activate

# Run database migrations
flask db upgrade
