#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <root_dir>"
    exit 1
fi

root_dir="$1"
# codebase_dir="$2"
i=0
j=0

for app_dir in "$root_dir"/application_*; do
    if [ -d "$app_dir" ]; then
       
        xml_files=("$app_dir"/*.xml)


        parsed_output_dir=$(find "$app_dir" -type d -name "parsed_output" | head -n 1)
        
        if [ -n "$parsed_output_dir" ]; then
            
            parent_dir=$(dirname "$parsed_output_dir")
            html_file="$parent_dir/diagnose report.html"
            if [ -f "$html_file" ]; then
                echo "$parent_dir identified as normal."
            else
                for xml_file in "${xml_files[@]}"; do
                    if [ -f "$xml_file" ]; then
                        log_file_start_time=$(date +%s)
                        dirfile="$parsed_output_dir/RCConfig_Direct.csv"
                        indirfile="$parsed_output_dir/RCConfig.csv"
                        find "$parsed_output_dir" -type f -name "*.out" -exec rm -f {} \;
                        find "$parsed_output_dir" -type f -name "*.log" -exec rm -f {} \;
                        find "$parsed_output_dir" -type f -name "*.txt" -exec rm -f {} \;
                        python3 /usr/local/LogConfigLocalizer/localizer/failure_diagnoser_with_des_with_direct.py -cp "$xml_file" -af "$parsed_output_dir"
                        log_file_end_time=$(date +%s)
                        time_file="$parsed_output_dir"/s2_total_time.log
                        echo $((log_file_end_time - log_file_start_time)) > "$time_file"
                    fi
                done
            fi
        fi
    fi
done

