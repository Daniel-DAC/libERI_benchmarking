#!/bin/bash

MASTER_SCRIPT="master_script.py"
SCRIPTS_DIR="scripts"

for dir in */; do
    if [ "$dir" == "$SCRIPTS_DIR/" ]; then
        continue
    fi

    for subdir in "$dir"*/; do
        if [ -d "$subdir" ]; then
            if [ -f "$subdir/$MASTER_SCRIPT" ]; then
                echo "Running $MASTER_SCRIPT in $subdir"
                (cd "$subdir" && python3 "$MASTER_SCRIPT" > master_log.txt 2>&1)
            else
                echo "Warning: $MASTER_SCRIPT not found in $subdir"
            fi
        fi
    done
done

