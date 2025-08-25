#!/bin/bash

# Name of the submission script
JOB_SCRIPT="bash_script_multiple"

# Loop through all directories in the current directory
for dir in */; do
    # Skip the Scripts directory
    if [ "$dir" == "Scripts/" ]; then
        continue
    fi

    # For each subdirectory of this directory
    for subdir in "$dir"*/; do
        # Check if it's a directory
        if [ -d "$subdir" ]; then
            echo "Submitting job in $subdir"

            # Check if the job script exists in the subdirectory
            if [ -f "$subdir/$JOB_SCRIPT" ]; then
                (cd "$subdir" && sbatch "$JOB_SCRIPT")
            else
                echo "Warning: No job script found in $subdir"
            fi
        fi
    done
done

