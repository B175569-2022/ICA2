#!/usr/bin/python3

# import modules
import os
import subprocess
import pandas as pd

# import my functions 
import functions as fun

# ask user if he wants to change working directory
fun.give_dir()

# ask user to define the protein family and taxonomic group (function outputs a dictionary)
prot_taxon = fun.give_prot_taxon()

# 
# if user provided a taxon name:
if (list(prot_taxon.keys())[1] == "taxon_name"):
  print("You want to search for a taxonmic group name:")
  print("Starting searching NCBI protein database for " + prot_taxon["protein"] + " in " + prot_taxon["taxon_name"] + ": ...\n")
  protein = prot_taxon["protein"]
  beast   = prot_taxon["taxon_name"]
  query   = protein + " [PROT] AND " + beast + " [organism]"     # get query string
  output  = protein.replace(" ", "_") + "_" + beast.replace(" ", "_") # output name (replace whitespace witj "_")
  esearch = 'esearch -db protein -query ' + '\"' + query + '\"'  # get esearch string ~ maybe give option to change database??
  # get fasta sequences:
  format  = 'fasta'
  efetch  = 'efetch -format ' + format + " > " + output + ".fa"  # get efetch string 
  full_search_cmd = esearch + " | " + efetch                     # get full cmd string
  print("Getting fasta sequences ...")
  print("Your esearch | efetch command:\n" + full_search_cmd)
  os.system(full_search_cmd)
  print("Done. Your fasta sequences are stored in: " + output + ".fa")
  # maybe more formats ???
#elif (list(prot_taxon.keys())[1] == "taxonid"):
#  print("You want to search for a taxonid:"
#  print("Starting searching NCBI protein database for " + prot_taxon["protein"] + " in " + prot_taxon["taxonid"] + ":")


# esearch -db protein -query "pyruvate dehydrogenase [PROT] AND ascomycete fungi [organism]" | efetch -format fasta > test-set.fa


