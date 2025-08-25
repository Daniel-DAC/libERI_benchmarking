#!/bin/bash

# Loop through all directories in the current directory
for dir in */; do
    # Skip specific directories
    [[ "$dir" == "Scripts/" || "$dir" == "Results/" ]] && continue

    # For each subdirectory of this directory
    for subdir in "$dir"*/; do
        # Check if it's a directory
        if [ -d "$subdir" ]; then
            echo "Checking $subdir for .csv files..."

            (
                cd "$subdir" || exit
                shopt -s nullglob
                csv_files=(*.csv)
                if [ ${#csv_files[@]} -gt 0 ]; then
                    echo "Removing: ${csv_files[*]}"
                    rm -v "${csv_files[@]}"
                else
                    echo "No .csv files found in $subdir"
                fi
                shopt -u nullglob
            )
        fi
    done
done

