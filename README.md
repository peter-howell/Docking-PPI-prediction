# PPI-pred-docking

Scripts used to predict protein-protein interactions based on docking models 
computed with GRAMM docking. This project was done for the course BCB 590:
Special Topics in Bioinformatics: The Bioinformatics of Host-Pathogen
Interactions.

First, folders for each pair of host and pathogen protein were created in 
`make_folders.sh`. This requires a list of all the names of host proteins be in
a file called `list_of_host_proteins.txt`, and the pathogen proteins likewise in
`list_of_pathogen_proteins.txt`. 

Each of the 70 pairs of proteins were submitted for GRAMM docking, and the job 
IDs were recorded in a file `job_ids.txt` with the interaction title and the job
ID on each line. 

The results from GRAMM docking were downloaded with `download_gramm_results.sh`
and programmatically searched against PDB for the 5 assemblies with the highest
structural simmilarity in `search_pdb.py`. Each docking complex was then aligned
with each of it's related PDB assemblies using TM-align, and the TM-score and 
RMSD were recorded in `run_TMalign.sh`. 

Then the scores were evaluated and visualized in `score_analysis.ipynb`.

