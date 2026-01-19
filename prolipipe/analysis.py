
import pandas as pd
import glob2 as glob
import os 

from prolipipe import utils

def read_list(file) :
    """
        Reads a list from a file, one element per line
    """
    list = []
    with open(file) as taxfile : 
        for line in taxfile : 
            list.append(line.strip())
    return list

def show_results (df_res) :
    """
        Extract and return never-found reactions while displaying maximum 
        completion observed 
    """
    ## get reactions never found 
    rxns_not_found = []
    rxns = [rxn for rxn in df_res.columns if "RXN" in rxn]
    for column in rxns : 
        if df_res[column].astype(int).sum() == 0  :
            rxns_not_found.append(column)

    ## get max percentage
    maxi = max(df_res["Possessed reactions"].to_list())
    reaction_nb = max(df_res["Total number of reactions"].to_list())
    ## few informations about reactions repartition
    print(f"\tmax. {maxi}/{reaction_nb} ; {len(rxns_not_found)} never found ({', '.join(reaction for reaction in rxns_not_found)})")
    
    return rxns_not_found

def add_columns(res_df, list_rxns, list_adj_rxns, col_filename="Filename") :
    """
        Add 4 columns from calculation to finish a result file :
        "Possessed reactions", 
        "Total number of reactions", 
        "Completion percent" and
        "Adj Compl Pct"
    """
    ## summing presences 
    res_df["Possessed reactions"] = res_df[list_rxns].sum(axis=1).astype(int)

    ## add total number of reactions
    res_df["Total number of reactions"] = [len(list_rxns) for file in res_df[col_filename]]

    ## add completion percentage
    res_df["Completion percent"] = (res_df["Possessed reactions"] / len(list_rxns) * 100).round(2)

    ## add adjusted completion percentage
    calcultate_adj_comp = (res_df["Possessed reactions"] / len(list_adj_rxns) * 100).round(2)
    res_df["Adj Compl Pct"] = calcultate_adj_comp if len(list_adj_rxns) != 0 else 100.0 

    return res_df

def template_df_from_taxfile (taxfile, genomes_processed, expected_cols): 
    """ 
        Furnish a template of result dataframe with the species, strain name 
        and file name as columns (data retrieved from strain and taxon files)
        Input : 
            taxfile (str) : path to taxon file 
            genomes_processed (list) : list of processed genomes 
        Output : 
            df (pd.DataFrame) : template df
    """
    ## get 5 columns from taxfile
    
    try:
        df = utils.rename_df(taxfile, expected_cols)

        ## limit it to processed genomes
        df = df[df["Filename"].isin(genomes_processed)]

        ## remove spaces from strain column 
        df["Strain"].apply(lambda x : x.replace(" ", "_"))

        ## return restricted and renamed df
        cols = ["Status", "Species", "Strain", "Filename"]

        return df[cols]
    
    except:
        print(f"Expect those columns in taxon_file : {", ".join(expected_cols)}")
        exit(1)

def generate_res_files(reactions_file, pwy_dir, taxfile, output, col_filename = "Filename") :
    """
        For each pathway file found in a given directory, build a result 
        file as Prolipipe output
        Input : 
            reaction_file (str) : path to reaction.tsv
            pwy_dir (str) : path to pathways directory
            taxfile (str) : path to taxon file 
            output (str) : path to output were tsv files will be written
            col_filename(str, optional) : header of the filenames column
        Output : 
            None, but files written  
    """
    ## explore pathways and prepare a list of all missing rxns 
    pwy_files = glob.glob(os.path.join(pwy_dir, "*.txt"))
    rxns_not_found = []

    ## get a transposed, renamed and restricted version of reactions.tsv
    df = pd.read_csv(reactions_file, sep='\t', header=0, low_memory=False, index_col=0)
    df = df.T.reset_index()
    df = df.rename(columns={"index" : col_filename})
    df = df[~df[col_filename].str.contains("_genes_assoc|_formula", na=False)]
    print(df, "\n", df.size)
    ## get template df with status, species, strain full name and filename 
    ## adapted to the number of processed genomes
    genomes_processed = df[col_filename].to_list()
    expected_cols = ["Species", "Taxon_id", "Filename", "Strain", "Status"]
    template_df = template_df_from_taxfile(taxfile, genomes_processed, expected_cols)

    for pwy_file in sorted(pwy_files):
        metabo = utils.my_basename(pwy_file)
        print(f"\n{metabo} : ")

        ## initialize result df, read rxns to process and rxns present at least once
        res_df = template_df.copy() 
        list_rxns = read_list(pwy_file)
        list_adj_rxns = [r for r in list_rxns]  ## not to change ; copy of list_rxns that may decrement

        ## adding reactions 
        for rxn in list(dict.fromkeys(list_rxns)) : ## remove reaction duplicates 
            if rxn in df.columns :  ## merging for reactions found
                to_incorporate = df[[col_filename,rxn]]
                res_df = pd.merge(res_df, to_incorporate, on=col_filename, how="left")

            else :                  ## filling with 0 for all filenames if not in reactions.tsv
                if len(res_df[expected_cols[2]]) == len(df[col_filename]):
                    res_df[rxn] = [0 for file in df[col_filename]]
                else :
                    if len(res_df[expected_cols[2]]) > len(df[col_filename]) : 
                        outlet_owner = "taxfile"
                        outlet = set(res_df[expected_cols[2]]) - set(df[col_filename])
                    else :
                        outlet_owner = "reaction file"
                        outlet =  set(res_df[expected_cols[2]]) - set(res_df[rxn])
                    message = f"Something is wrong between the number of columns of your reaction file {reactions_file} \nand your taxa file {taxfile}."
                    message += f"\nAn outlet is found in the {outlet_owner} : '{outlet}'. Please remove/add it to make files columns matching."
                    raise ValueError(message)

        ## adding calculation columns
        res_df = add_columns(res_df, list_rxns, list_adj_rxns, col_filename)
        
        ## concatenate reactions not found 
        rxns_not_found = rxns_not_found + show_results (res_df)

        filename = os.path.join(output, metabo + ".tsv")
        res_df.to_csv(filename, sep = "\t", index = False)
        print(f"\t-> saved in {filename}\n")

    print(f"\nIn total, {len(set(rxns_not_found))} reactions never found in genomes : \n{', '.join(rxn for rxn in rxns_not_found)})")

    
def test_df (df_prol, df_new, col_filename="Filename") :
    """
    Compare df content between 2 dfs, shows non-matching rows
    """
    import numpy as np
    df_prol = pd.read_csv(df_prol, sep = "\t").sort_values(by="reaction", ascending=True)
    df_new = pd.read_csv(df_new, sep = "\t").sort_values(by=col_filename, ascending=True)
    cols = [rxn for rxn in df_prol.columns if "RXN" in rxn] + ["Completion percent", "Adj Compl Pct"]

    for i in range (len(df_prol)) : 
        for col in cols : 
            if not np.isclose(df_prol.at[i, col], df_new.at[i, col], atol=1e-8):
                print(f"\nDefault found in {col}:")
                # print(f"\t{list(df_prol.columns)}")
                print(f"\t{list(df_prol.iloc[i])}\n")
                # print(f"\t{list(df_new.columns)}")
                print(f"\t{list(df_new.iloc[i])}\n")
