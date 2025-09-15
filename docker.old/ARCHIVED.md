# Archived Docker Directory

This directory contains the old Docker configuration that has been superseded.

## Migration Date
September 14, 2025

## What Changed
- Moved `Dockerfile.inference` → root `Dockerfile`
- Moved `docker-compose.yml` → root
- Created root `.dockerignore`
- Created unified `Makefile` in root

## Files Here
These files are kept for reference but are no longer used:
- Multiple Dockerfile variants (test, minimal, nedc)
- Old Makefile.docker
- Original docker-compose configuration

## New Location
All active Docker configuration is now in the repository root:
- `/Dockerfile` - Main container
- `/docker-compose.yml` - Orchestration
- `/.dockerignore` - Build exclusions
- `/Makefile` - Unified commands including Docker targets

This directory can be safely deleted once we confirm the new setup works.