# 🔧 DOCKER FIX PLAN
## Getting Docker Working Without Breaking Our 65GB Data

## The Problem
- 65GB of TUSZ/Siena data in `wu_2025/data/`
- Docker tries to copy ALL of it into build context
- .dockerignore not preventing the copy
- Builds timeout or fail

## The Solution

### Step 1: Data Strategy
**NEVER put data in Docker image!**
- Keep data on host filesystem
- Mount as read-only volumes at runtime
- Use sample data for testing

### Step 2: Fix .dockerignore
```
# Must exclude ALL data
wu_2025/data/**
experiments/**
*.edf
*.pkl
*.checkpoint
```

### Step 3: Test Strategy
```bash
# 1. Create tiny test data
mkdir -p test_data/sample
cp wu_2025/data/tusz/v2.0.3/edf/eval/01_tcp_ar/002/00000258/*.edf test_data/sample/

# 2. Build without any data
docker build -t seizure:test .

# 3. Run with volume mount
docker run --gpus all -v $(pwd)/test_data:/data:ro seizure:test
```

### Step 4: Production Strategy
```yaml
# docker-compose.yml
services:
  seizure:
    volumes:
      # Mount real data as read-only
      - /mnt/c/Users/JJ/Desktop/Clarity-Digital-Twin/SeizureTransformer/wu_2025/data:/data:ro
```

## Safe Testing Commands

```bash
# Test 1: Verify data is excluded
docker build -f Dockerfile -t test1 . --dry-run

# Test 2: Check build context size
tar -czf - . --exclude='wu_2025/data' --exclude='experiments' | wc -c

# Test 3: Mini build
echo "FROM ubuntu:22.04" > Dockerfile.mini
echo "RUN echo 'works'" >> Dockerfile.mini
docker build -f Dockerfile.mini -t mini .
```

## DO NOT:
- Move or delete the 65GB data
- Include data in Docker image
- Use sudo with data operations
- Build without checking context size first

## Current Status
- ✅ Data is safe at `wu_2025/data/`
- ❌ Docker builds failing due to data size
- 🔧 Need to fix .dockerignore and test with volumes