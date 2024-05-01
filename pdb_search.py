import os
import glob
from rcsbsearchapi.search import StructSimilarityQuery
import requests
# import pandas as pd
import gzip
import shutil


def gunzip_file(gzipped_file:str, output_file:str):
    with gzip.open(gzipped_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(gzipped_file)

def pdb_downloaded(pdb_id:str) -> bool:
    """check to see if the given pdb file has been downloaded to PDB_matches already

    Args:
        pdb_id (str): id to check for

    Returns:
        bool: `True` if the file exists in PDB_matches, otherwise `False`
    """
    return os.path.exists(f"data/PDB_matches/{pdb_id}")

def get_potential_interactions(search_loc = "data/GRAMM_docking_results") -> list[str]:
    """get all folders in the GRAMM_docking_results directory

    Args:
        search_loc (str, optional): Where to look for the interations. Defaults to "GRAMM_docking_results".

    Returns:
        list[str]: list of folder names signifying the interactions between host and pathogen proteins
    """
    interxns = []
    for item in os.listdir(search_loc):
        item_location = "%s/%s" % (search_loc, item)
        if os.path.isdir(item_location):
            interxns.append(item)
    return interxns

def find_gramm_models(interxn:str, search_loc = "data/GRAMM_docking_results") -> list[str]:
    """get all the GRAMM docking models for a given interaction

    Args:
        interxn (str): the name of the interaction. eg: `Sap1_x_IL1A`

    Returns:
        list[str]: list pdb files of the gramm docking models for the given interaction
    """
    search = f"{search_loc}/{interxn}/GRAMMresults/receptor-ligand_model*"
    return glob.glob(search)

def search_pdb(gramm_file:str) -> list[str]:
    """creates a list of up to 5 PDB ids of assemblies that are similar to the structure in the given file

    Args:
        gramm_file (str): PDB file of the GRAMM docking

    Returns:
        list[str]: list of PDB ids
    """
    q1 = StructSimilarityQuery(structure_search_type="file_upload",
                        file_path=gramm_file,
                        file_format="pdb",
                        operator="strict_shape_match",
                        target_search_space="assembly")
    items = []
    for i, item in enumerate(q1("assembly")):
        if i < 5:
            # We are searching for assemblies. it returns a pdb code followed 
            # by the assembly number, so for example 6M6T-3.
            # The files for these are named 6M6T.pdb3.gz so we split at the 
            # hyphen for when we download file later.
            x = item.split("-")
            items.append(f"{x[0]}.pdb{x[1]}")
    return items

def download_pdb(pdb_ids: list[str]):
    """download a (set of) PDB file(s)

    Args:
        pdb_ids (list[str]): file(s) to download
    """
    if isinstance(pdb_ids, str):
        # if given a single id, put it in list
        pdb_ids = [pdb_ids]
    for id in pdb_ids:
        file_out = f"data/PDB_matches/{id}"
        file_gz = f"{file_out}.gz"
        if os.path.exists(file_out):
            # file already exists, don't need to download it again
            continue
        url = f"https://files.rcsb.org/download/{id}.gz"
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_gz, 'wb') as f:
                f.write(response.content)
            gunzip_file(file_gz, file_out)
        else:
            print(f"Failed to download PDB file {id}. Status code: {response.status_code}")
            # print(url)

potential_interxns = get_potential_interactions()

gramm_models = {}
for interxn in potential_interxns:
    gramm_models[interxn] = find_gramm_models(interxn)

gramm_x_pdb = {}
for models in list(gramm_models.values()):
    for model in models:
        gramm_x_pdb[model] = search_pdb(model)

for pdbs in gramm_x_pdb.values():
    download_pdb(pdbs)


with open("data/interaction_info.tsv", "w") as f:
    for interxn in sorted(potential_interxns):
        x = interxn.split("_")
        path_prot = x[0]
        host_prot = x[2]
        for gramm_model in gramm_models[interxn]:
            for related_pdb in gramm_x_pdb[gramm_model]:
                if pdb_downloaded(related_pdb):
                    f.writelines(f"{path_prot}\t{host_prot}\t{gramm_model}\tPDB_matches/{related_pdb}\n")
