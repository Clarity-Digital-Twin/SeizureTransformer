# Docker Infrastructure (Future Work)

This directory contains Docker configurations for future containerized deployment.

## Status
**🚧 Under Development** - These Docker files are not yet production-ready due to data volume handling issues (65GB TUSZ dataset).

## Files
- `Dockerfile` - Basic container setup
- `Dockerfile.inference` - GPU-enabled inference container
- `Dockerfile.nedc` - NEDC scoring environment
- `Dockerfile.minimal` - Lightweight test container
- `docker-compose.yml` - Multi-service orchestration
- `Makefile.docker` - Docker build commands

## Known Issues
- Need to implement proper volume mounting for large datasets
- GPU passthrough configuration needs testing
- NEDC binary compatibility in containers

## Future Implementation
See `docs/planning/DOCKER_FIX_PLAN.md` for the roadmap to fix Docker deployment.