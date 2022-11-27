#!/usr/bin/python3

# import modules
import os, subprocess, sys, re
import pandas as pd

# import my functions 
import functions as fun

# ask user if he wants to change working directory
fun.give_dir()

# ask user to define the protein family and taxonomic group (function outputs a dictionary)
prot_taxon = fun.give_prot_taxon()

# pyruvate dehydrogenase
# ascomycete fungi
# 

# if user provided a taxon name:
if (list(prot_taxon.keys())[1] == "taxon_name"):
  print("You want to search for a taxonomic group name:")
  print("Starting searching NCBI protein database for " + prot_taxon["protein"] + " in " + prot_taxon["taxon_name"] + ": ...\n")
  protein = prot_taxon["protein"]
  beast   = prot_taxon["taxon_name"]
  query   = protein + " [PROT] AND " + beast + " [organism]"     # get query string
  search_out  = protein.replace(" ", "_") + "_" + beast.replace(" ", "_") # search output name (replace whitespace witj "_")
  esearch = 'esearch -db protein -query ' + '\"' + query + '\"'  # get esearch string ~ maybe give option to change database??
  # get fasta sequences:
  search_out_fasta = search_out + ".fa"                          # fasta file output name (used later)
  format  = 'fasta'
  efetch  = 'efetch -format ' + format + " > " + search_out_fasta# get efetch string 
  full_search_cmd = esearch + " | " + efetch                     # get full cmd string
  print("Getting fasta sequences ...")
  print("Your esearch | efetch command:\n" + full_search_cmd)
  os.system(full_search_cmd)
  print("Done. Your fasta sequences are stored in: " + search_out_fasta)
  # get accession numbers:
  #output_acc = output + ".acc"                                 # accessions file output name (used later)
  #format  = 'acc'
  #efetch  = 'efetch -format ' + format + " > " + output_acc    # get efetch string 
  #full_search_cmd = esearch + " | " + efetch                   # get full cmd string
  #print("Getting accession numbers of sequences ...")
  #print("Your esearch | efetch command:\n" + full_search_cmd)
  #os.system(full_search_cmd)
  #print("Done. Your sequences's accession numbers are stored in: " + output_acc)


#elif (list(prot_taxon.keys())[1] == "taxonid"):
#  print("You want to search for a taxonid:"
#  print("Starting searching NCBI protein database for " + prot_taxon["protein"] + " in " + prot_taxon["taxonid"] + ":")


# esearch -db protein -query "pyruvate dehydrogenase [PROT] AND ascomycete fungi [organism]" | efetch -format fasta > test-set.fa


################################## Ask questions about search output ######################################

### read .fa file 
# count no of sequences based on the number of headers in the .fa file 
#fasta = open('pyruvate_dehydrogenase_ascomycete_fungi.fa', 'r')  ### change !!!! to search_out_fasta
fasta = open(search_out_fasta, 'r')
seqs_count = 0     # counter for sequences
species_dict = {}  # dict to count no. of accurances for each species: species_dict = {species1: no of appearances,...} -> no of keys = no of species
for line in fasta:
  line = line.rstrip("\n")    # read each line, strip '\n' at the end
  if re.search(r'^>', line):  # get header lines (start with ">")
    #print(line)
    #header_line = line
    ## count no. of sequences  
    seqs_count += 1
    ## get species name 
    species = re.search(r'.*?\[(.*)].*', line).group(1)         # exract species name from header (inside square brackets) - use as key
    #print(species)
    species_dict[species] = species_dict.get(species,0) + 1     # if first time, set value of dict to 0 then add 1.+ 1 every time species seen again 
  #else:
  #  print(line)

fasta.close()

### ask user if they want to continue. exit if no sequences are found
if (seqs_count == 0):
  print("Warning: You have found NO protein sequences. You may want to refine you searching criteria and try again. Exiting analysis ...")
  sys.exit()
elif (seqs_count > 1000):
  q_seqs = input("Warning: You have found " + str(seqs_count) + " protein sequences, this may be too many. Do you want to continue with analysis? (y/n)")
elif (seqs_count < 10):
  q_seqs = input("Warning: You have found " + str(seqs_count) + " protein sequences, this may be too few. Do you want to continue with analysis? (y/n)")
elif (seqs_count < 1000):
  q_seqs = input("You have found " + str(seqs_count) + " protein sequences. This is an acceptable amount. Do you want to continue with analysis? (y/n)")

if (q_seqs.lower() == "n"):
  print("Exiting ...")
  sys.exit()

### ask user if number of species is ok
no_of_species = len(species_dict.keys())                                                  # number of species, each key a different species
top_species   = [i for i in species_dict if species_dict[i]==max(species_dict.values())]  # most frequent species (may be > 1)

if (input("Your dataset has " + str(no_of_species) + " species. Do you wish to continue? (y/n)").lower() == "n"):
  print("Exiting ...")
  sys.exit()

# which species is the most frequent, how many sequences. ask if ok
if (input("Species " + str(top_species) + " is the most frequent with " + str(max(species_dict.values())) + " sequences in the dataset. Is this ok? (y/n)").lower() == "n"):
  print("Exiting ...")
  sys.exit()


################################## align sequences (clustalo) ######################################

try 




