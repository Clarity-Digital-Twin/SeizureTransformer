#!/bin/bash
# Data Migration Script for Docker Compatibility
# Moves 80GB of data OUT of wu_2025/ to enable Docker builds

set -e  # Exit on error

echo "=== SeizureTransformer Data Migration ==="
echo "This script moves large datasets out of the codebase for Docker compatibility"
echo ""
echo "Current data sizes:"
du -sh wu_2025/data/tusz 2>/dev/null || echo "  TUSZ: not found"
du -sh wu_2025/data/siena 2>/dev/null || echo "  Siena: not found"
echo ""

# Confirm before proceeding
read -p "This will move ~80GB of data. Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Create root data directory
echo "Creating root data directory..."
mkdir -p data

# Move TUSZ dataset (62GB)
if [ -d "wu_2025/data/tusz" ] && [ ! -L "wu_2025/data/tusz" ]; then
    echo "Moving TUSZ dataset (62GB)..."
    echo "  From: wu_2025/data/tusz"
    echo "  To:   data/tusz"
    mv wu_2025/data/tusz data/
    echo "Creating symlink for backward compatibility..."
    ln -s ../../data/tusz wu_2025/data/tusz
    echo "✓ TUSZ migration complete"
else
    echo "⚠ TUSZ already migrated or is a symlink"
fi

# Move Siena dataset (18GB)
if [ -d "wu_2025/data/siena" ] && [ ! -L "wu_2025/data/siena" ]; then
    echo "Moving Siena dataset (18GB)..."
    echo "  From: wu_2025/data/siena"
    echo "  To:   data/siena"
    mv wu_2025/data/siena data/
    echo "Creating symlink for backward compatibility..."
    ln -s ../../data/siena wu_2025/data/siena
    echo "✓ Siena migration complete"
else
    echo "⚠ Siena already migrated or is a symlink"
fi

# Update .gitignore to exclude data
echo "Updating .gitignore..."
if ! grep -q "^data/$" .gitignore 2>/dev/null; then
    echo "" >> .gitignore
    echo "# Large datasets (use volume mounts)" >> .gitignore
    echo "data/" >> .gitignore
    echo "✓ Updated .gitignore"
fi

# Verify symlinks work
echo ""
echo "Verifying symlinks..."
if [ -L "wu_2025/data/tusz" ]; then
    echo "✓ TUSZ symlink: $(readlink wu_2025/data/tusz)"
fi
if [ -L "wu_2025/data/siena" ]; then
    echo "✓ Siena symlink: $(readlink wu_2025/data/siena)"
fi

# Final summary
echo ""
echo "=== Migration Complete ==="
echo "Data is now at:"
echo "  ./data/tusz  (62GB)"
echo "  ./data/siena (18GB)"
echo ""
echo "Symlinks created for backward compatibility:"
echo "  wu_2025/data/tusz  -> ../../data/tusz"
echo "  wu_2025/data/siena -> ../../data/siena"
echo ""
echo "Docker builds will now work! The data is excluded from build context."
echo ""
echo "To use Docker with data:"
echo "  docker run -v \$(pwd)/data:/app/data ..."