#!/bin/bash

# Check if both files exist
if [ ! -f "list_of_pathogen_prots.txt" ] || [ ! -f "list_of_host_prots.txt" ]; then
    echo "One or both input files do not exist."
    exit 1
fi

# Read proteins from files into arrays
while IFS= read -r pathogen_protein || [[ -n "$pathogen_protein" ]]; do
    pathogen_proteins+=("$pathogen_protein")
done < "list_of_pathogen_prots.txt"

while IFS= read -r host_protein || [[ -n "$host_protein" ]]; do
    host_proteins+=("$host_protein")
done < "list_of_host_prots.txt"

# Create directories for each pair of proteins
for pathogen_protein in "${pathogen_proteins[@]}"; do
    for host_protein in "${host_proteins[@]}"; do
        dir_name="${pathogen_protein%$'\n'}_x_${host_protein%$'\n'}"
        mkdir "$dir_name"
    done
done
