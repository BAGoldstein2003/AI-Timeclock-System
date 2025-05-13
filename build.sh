#!/usr/bin/env bash

# Exit immediately if any command fails
set -e

# Update system packages and install build dependencies for dlib
apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libboost-all-dev \
    python3-dev \
    pkg-config \
    libopenblas-dev \
    liblapack-dev

# Install Python dependencies
pip install -r requirements.txt