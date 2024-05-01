#!/bin/bash

job_ids_file="job_ids.txt"

# Loop through each line in the file
while IFS= read -r line; do
    # Extract folder name and job ID from the line
    folder_name=$(echo "$line" | awk '{print $1}')
    folder_name=data/GRAMM_docking_results/$folder_name
    job_id=$(echo "$line" | awk '{print $2}')

    if [ ! -d "$folder_name" ]; then
       mkdir "$folder_name"
    fi

    # Construct the download URL
    download_url="https://gramm.compbio.ku.edu/download/$job_id/0"

    # Use wget to download the zip file
    wget -q "$download_url" -O "GRAMMresults.zip"

    unzip GRAMMresults.zip
    rm GRAMMresults.zip
    
    if [ -d "$folder_name"/GRAMMresults ]; then
        rm -rf "$folder_name"/GRAMMresults
    fi
    
    mv GRAMMresults "$folder_name"/GRAMMresults

done < "$job_ids_file"
