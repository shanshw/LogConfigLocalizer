#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <root_dir> <codebase_dir>"
    exit 1
fi

root_dir="$1"
codebase_dir="$2"
i=0
start_time=$(date +%s)
for app_dir in "$root_dir"/application_*; do
    if [ -d "$app_dir" ]; then
        xml_files=("$app_dir"/*.xml)
        parsed_output_dir=$(find "$app_dir" -type d -name "parsed_output" | head -n 1)
        if [ -n "$parsed_output_dir" ]; then
            echo "Found 'parsed_output' directory: $parsed_output_dir"
            # html_file=
            python3 /usr/local/LogConfigLocalizer/localizer/anomaly_identifier.py -fp "$codebase_dir" -mp "$parsed_output_dir"
            ((i++))
            
        fi
    fi
done
end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

echo "End of script"
echo "Elapsed time: ${elapsed_time} seconds"
echo "Total: $i files"