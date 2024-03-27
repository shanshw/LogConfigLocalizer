#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <root_dir>"
    exit 1
fi

root_dir="$1"
for app_dir in "$root_dir"/application_*; do
    if [ -d "$app_dir" ]; then
        xml_files=("$app_dir"/*.xml)
        parsed_output_dir=$(find "$app_dir" -type d -name "parsed_output" | head -n 1) 
        if [ -n "$parsed_output_dir" ]; then
            # echo "Found 'parsed_output' directory: $parsed_output_dir"           
            for xml_file in "${xml_files[@]}"; do
                if [ -f "$xml_file" ]; then
                    echo "Found XML file: $xml_file"
                    dirfile="$parsed_output_dir/RCConfig_Direct.csv"
                    indirfile="$parsed_output_dir/RCConfig.csv"
                    if [ -f "$dirfile" ] && [ -f "$indirfile" ]; then
                        echo "Found Both RCConfig_Direct.csv file: $dirfile, and RCConfig.csv file: $indirfile"
                        python3 /usr/local/LogConfigLocalizer/localizer/util/gen_bug_report.py -rc "$indirfile" -anomaly True
                    elif [ -f "$dirfile" ]; then
                        echo "Found Only RCConfig_Direct.csv file: $dirfile"
                        python3 /usr/local/LogConfigLocalizer/localizer/util/gen_bug_report.py -rc "$dirfile" -anomaly True
                    elif [ -f "$indirfile" ]; then
                        echo "Found Only RCConfig.csv file: $indirfile"
                        python3 /usr/local/LogConfigLocalizer/localizer/util/gen_bug_report.py -rc "$indirfile" -anomaly True
                    else
                        echo "Normal: $parsed_output_dir"
                    fi
                fi
            done
        fi
    fi
done
