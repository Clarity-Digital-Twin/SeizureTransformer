#!/bin/bash
# Production Pipeline Runner for SeizureTransformer
# Complete end-to-end evaluation with proper error handling
# Date: September 2025

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# ============================================================================
# Configuration
# ============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
DATA_DIR="${DATA_DIR:-$PROJECT_ROOT/data}"
EXPERIMENTS_DIR="${EXPERIMENTS_DIR:-$PROJECT_ROOT/experiments}"
DOCKER_IMAGE="seizure-transformer:latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================================================
# Helper Functions
# ============================================================================
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker not found. Please install Docker."
        exit 1
    fi

    # Check data directory
    if [ ! -d "$DATA_DIR" ]; then
        log_error "Data directory not found: $DATA_DIR"
        exit 1
    fi

    # Check for TUSZ data
    if [ ! -d "$DATA_DIR/tusz/edf/eval" ]; then
        log_warn "TUSZ eval data not found at $DATA_DIR/tusz/edf/eval"
        log_warn "Please ensure data is properly downloaded and extracted"
    fi

    # Create experiments directory
    mkdir -p "$EXPERIMENTS_DIR"

    log_info "Prerequisites check passed"
}

build_docker_image() {
    log_info "Building Docker image..."

    docker build \
        --tag "$DOCKER_IMAGE" \
        --file "$PROJECT_ROOT/Dockerfile" \
        "$PROJECT_ROOT" || {
        log_error "Docker build failed"
        exit 1
    }

    log_info "Docker image built successfully"
}

validate_data() {
    log_info "Validating data..."

    docker run \
        --rm \
        -v "$DATA_DIR:/data:ro" \
        "$DOCKER_IMAGE" \
        python /app/scripts/validate_data.py \
        --data_dir /data/tusz/edf/eval \
        --check_channels \
        --check_format || {
        log_warn "Data validation found issues (continuing anyway)"
    }
}

run_evaluation() {
    log_info "Running evaluation pipeline..."

    local output_dir="$EXPERIMENTS_DIR/run_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$output_dir"

    docker run \
        --rm \
        -v "$DATA_DIR:/data:ro" \
        -v "$output_dir:/experiments:rw" \
        "$DOCKER_IMAGE" \
        eval \
        --data_dir /data/tusz/edf/eval \
        --out_dir /experiments \
        --device auto || {
        log_error "Evaluation failed"
        exit 1
    }

    log_info "Evaluation complete. Results in: $output_dir"
    echo "$output_dir" > "$EXPERIMENTS_DIR/latest_run.txt"
}

run_nedc_scoring() {
    log_info "Running NEDC scoring..."

    local latest_run=$(cat "$EXPERIMENTS_DIR/latest_run.txt")

    if [ ! -f "$latest_run/checkpoint.pkl" ]; then
        log_error "Checkpoint not found: $latest_run/checkpoint.pkl"
        exit 1
    fi

    docker run \
        --rm \
        -v "$latest_run:/experiments:rw" \
        "$DOCKER_IMAGE" \
        nedc \
        --checkpoint /experiments/checkpoint.pkl \
        --outdir /experiments/nedc_results \
        --backend native-overlap || {
        log_error "NEDC scoring failed"
        exit 1
    }

    log_info "NEDC scoring complete"
}

print_results() {
    local latest_run=$(cat "$EXPERIMENTS_DIR/latest_run.txt")

    if [ -f "$latest_run/nedc_results/metrics.json" ]; then
        log_info "Results:"
        cat "$latest_run/nedc_results/metrics.json" | python -m json.tool
    else
        log_warn "No results found"
    fi
}

# ============================================================================
# Main Pipeline
# ============================================================================
main() {
    echo "=================================================="
    echo "SeizureTransformer Production Pipeline"
    echo "=================================================="

    # Parse arguments
    case "${1:-full}" in
        build)
            check_prerequisites
            build_docker_image
            ;;
        validate)
            check_prerequisites
            validate_data
            ;;
        eval)
            check_prerequisites
            run_evaluation
            ;;
        score)
            check_prerequisites
            run_nedc_scoring
            ;;
        results)
            print_results
            ;;
        full)
            check_prerequisites
            build_docker_image
            validate_data
            run_evaluation
            run_nedc_scoring
            print_results
            ;;
        *)
            echo "Usage: $0 {build|validate|eval|score|results|full}"
            echo ""
            echo "  build    - Build Docker image"
            echo "  validate - Validate data files"
            echo "  eval     - Run evaluation pipeline"
            echo "  score    - Run NEDC scoring"
            echo "  results  - Display results"
            echo "  full     - Run complete pipeline (default)"
            exit 1
            ;;
    esac

    log_info "Pipeline complete!"
}

# Run main function
main "$@"