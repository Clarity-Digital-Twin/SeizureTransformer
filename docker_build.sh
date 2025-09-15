#!/bin/bash
echo "Starting Docker build at $(date)"
export DOCKER_BUILDKIT=0

echo "Build context size:"
du -sh . --exclude=.git --exclude=data --exclude=experiments --exclude=.venv 2>/dev/null || echo "Could not calculate"

echo "Starting Docker build..."
docker build -t seizure-transformer:latest . 2>&1
echo "Build completed at $(date)"
