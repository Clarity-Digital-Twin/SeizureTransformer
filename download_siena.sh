#!/bin/bash
# Download Siena Scalp EEG Database for SeizureTransformer paper parity

echo "Starting download of Siena Scalp EEG Database (13GB)..."
echo "This will take a while depending on your connection speed."

cd data/datasets/siena

# Download all files recursively
wget -r -N -c -np --no-host-directories --cut-dirs=3 \
     --accept "*.edf,*.txt,*.csv,LICENSE.txt,RECORDS,SHA256SUMS.txt" \
     https://physionet.org/files/siena-scalp-eeg/1.0.0/

echo "Download complete!"
echo "Files saved to: data/datasets/siena/"

# Show what was downloaded
echo "Downloaded structure:"
ls -la

