#!/usr/bin/python3

# import modules
import os, subprocess, sys, re
#import pandas as pd

# import my functions 
import functions as fun

### read .fa file 
# count no of sequences based on the number of headers in the .fa file 
fasta = open('pyruvate_dehydrogenase_ascomycete_fungi.fa', 'r')
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
  #  print("no header line")

fasta.close()

### ask user if they want to continue. exit if no sequences are found
if (seqs_count > 1000):
  q_seqs = input("Warning: You have found " + str(seqs_count) + " protein sequences, this may be too many. Do you want to continue with analysis? (y/n)")
elif (seqs_count == 0):
  print("Warning: You have found NO protein sequences. You may want to refine you searching criteria and try again. Exiting analysis ...")
  sys.exit()
elif (seqs_count < 1000):
  q_seqs = input("You have found " + str(seqs_count) + " protein sequences. This is an acceptable amount. Do you want to continue with analysis? (y/n)")

if (q_seqs == "n"):
  print("Exiting ...")
  sys.exit()

### ask user if number of species is ok
no_of_species = len(species_dict.keys())                                                  # number of species, each key a different species
top_species   = [i for i in species_dict if species_dict[i]==max(species_dict.values())]  # most frequent species (may be > 1)

if (input("Your dataset has " + str(no_of_species) + " species. Do you wish to continue? (y/n)") == "n"):
  print("Exiting ...")
  sys.exit()

# which species is the most frequent, how many sequences. ask if ok
if (input("Species " + str(top_species) + " is the most frequent with " + str(max(species_dict.values())) + " sequences in the dataset. Is this ok? (y/n)") == "n"):
  print("Exiting ...")
  sys.exit()




#with open("pyruvate_dehydrogenase_ascomycete_fungi.fa") as fasta:
#  fasta_contents = fasta.read()
  
  #for line in fasta_contents:
  #  print(line)
    #if re.search(r'^>', line):
    #  print(line)
    #else:
    #  print("no header")
      


    