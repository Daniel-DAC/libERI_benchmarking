#!/bin/bash

# Define the name of the scripts directory
SCRIPTS_DIR="scripts"

# Get the full path to the scripts directory
SCRIPTS_PATH="$(pwd)/$SCRIPTS_DIR"

# Check if the Scripts directory exists
if [ ! -d "$SCRIPTS_PATH" ]; then
    echo "Error: '$SCRIPTS_DIR' directory not found in $(pwd)"
    exit 1
fi

# Loop over all items in the current directory
for dir in */; do
    # Skip the Scripts directory
    if [ "$dir" == "$SCRIPTS_DIR/" ]; then
        continue
    fi

    # For each subdirectory of this directory
    for subdir in "$dir"*/; do
        # Check if it's a directory
        if [ -d "$subdir" ]; then
            echo "Copying scripts to $subdir"
            cp "$SCRIPTS_PATH"/* "$subdir"
        fi
    done
done

