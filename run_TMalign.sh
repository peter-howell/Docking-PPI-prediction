#!/bin/bash

data_file="interaction_info.tsv"
temp_aln_file="temp.log"

results_file="TM_results.tsv"

touch "$results_file"
rm "$results_file"
echo -e "sap\thost_protein\tgramm_model\tknown_model\tTMscore\tRMSD" > "$results_file"

while IFS= read -r line; do
    sap=$(echo "$line" | awk '{print $1}')
    host_prot=$(echo "$line" | awk '{print $2}')
    gramm_model=$(echo "$line" | awk '{print $3}')
    known_model=$(echo "$line" | awk '{print $4}')
    
    TMalign "$gramm_model" "$known_model" > $temp_aln_file

    tmscore=$(grep "TM-score" $temp_aln_file | awk '{print $2}' | head -n 1)
    RMSD=$(grep "RMSD" $temp_aln_file | awk '{print $5}' | sed 's/,$//' | head -n 1)

    echo -e "$sap\t$host_prot\t$gramm_model\t$known_model\t$tmscore\t$RMSD" >> "$results_file"
done < "$data_file"

rm "$temp_aln_file"
