#!/bin/bash

# Name of the output directory
RESULTS_DIR="Results"

# Create the Results directory if it doesn't exist
mkdir -p "$RESULTS_DIR"

# Find and copy all gamess_summary_*.csv files from subdirectories
find . -type f -name "*.csv" | while read -r file; do
    # Get just the filename (without path)
    filename=$(basename "$file")
    
    # Copy to Results/, overwriting if it already exists
    cp "$file" "$RESULTS_DIR/$filename"
    
    echo "Copied $file → $RESULTS_DIR/$filename"
done

