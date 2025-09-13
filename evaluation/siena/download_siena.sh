#!/bin/bash
# Download Siena Scalp EEG Database to CORRECT location for SeizureTransformer

echo "Starting download of Siena Scalp EEG Database (13GB) to wu_2025/data/siena..."
echo "This will take a while depending on your connection speed."

cd wu_2025/data/siena

# Download all files recursively with proper flags
wget -r -N -c -np --no-host-directories --cut-dirs=3 \
     --accept "*.edf,*.txt,*.csv,LICENSE.txt,RECORDS,SHA256SUMS.txt" \
     https://physionet.org/files/siena-scalp-eeg/1.0.0/

echo "Download complete!"
echo "Files saved to: wu_2025/data/siena/"

# Show summary
echo "Downloaded structure:"
du -sh .
ls -la

