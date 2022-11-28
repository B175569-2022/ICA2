#!/usr/bin/python3

# import modules
import os, subprocess, sys, re
import pandas as pd

# import my functions 
import functions as fun

# ask user if he wants to change working directory
fun.give_dir()

################################## Obtain user-defined protein sequences ######################################

# ask user to define the protein family and taxonomic group (function outputs a dictionary)
prot_taxon = fun.give_prot_taxon()
#prot_taxon = {"protein": "pyruvate dehydrogenase", "taxon_name": "ascomycete fungi"}


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

### print number of sequences found. Ask user if they want to continue. exit if no sequences are found
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

################################## Ask to remove redundant sequences (skipredundant) ######################################

# will ask for input until user gives a valid answer (y or n)
# not 'y' or 'n' => else: sys.exit() => error => except => while loop from the beginning => ask for input => ... => corrrect input => break while loop
while True:
  q_red = input("Do you want to remove redundant sequences (highly similar) or sequences within a % similarity threshold range? (y/n)\n").lower()
  #print(q_red)
  try:
    if (q_red == "n"):
      print("Continuing with the full set of " + str(seqs_count) + " protein sequences.\n")
    elif (q_red == "y"):
      print("Initiating analysis to remove redundant sequences ...\n")      
    else:
      sys.exit()
  except:
    print("I didn't understand that. Please type 'y' or 'n'.")
    continue
  else:
    # no errors, exit loop
    break

### set arguement for skipredundant 
if (q_red == 'y'):
  print("will use skipredundant for this ...\n")
  # give mode arguement & test if input is correct
  while True:
    mode = input("Do you want only an upper threshold for sequence similarity? (1)\nOr a lower & upper range of sequence similarity (2)? Press 1 or 2:")
    try:
      mode = int(mode) # tests if integer
    except ValueError:
      print("I didn't understand that. Please type an integer: 1 or 2.") 
      continue
    else:
      break
  # give (max) threshold & test if input is correct
  while True:
    threshold = input("What is the upper % sequence identity that you want [default=90.0]? Give float/integer number.")
    try:
      threshold = float(threshold)
    except ValueError:
      print("I didn't understand that. Please type a integer/float number for upper % similarity.")
      continue
    else:
      break
  # give min threshold if in mode 2 & test if input is correct
  if (mode == 2):
    while True:
      #maxthreshold = threshold
      minthreshold = input("What is the lower % sequence identity that you want [default=20.0]? Give float/integer number.")
      try:
        minthreshold = float(minthreshold)
      except ValueError:
        print("I didn't understand that. Please type a float/integer number for lower % similarity.")
        continue
      else:
        break
  elif (mode == 1):
      print("No min threshold requested")
      minthreshold = 20.0 # this will not be used. set as default to avoid errors when calling the function fun.run_skipredundant()
  # input name(.fa file from search)
  skipredundant_in_fasta = search_out + ".fa"
  # output name (.fa file of non-redundant seqs - will be kept)
  skipredundant_out_fasta = search_out + ".keep"
  print("will write non-redundant seqs to keep in: " + skipredundant_out_fasta)
  # output name (.fa file of redundant seqs - will be excluded)
  skipredundant_out_fasta_red = search_out + ".not.keep"
  print("will write redundant seqs not to keep in: " + skipredundant_out_fasta_red)
  # run skipredundant with set parameters
  print("Running skipredundant. This may take a few minutes ...\n") 
  fun.run_skipredundant(skipredundant_in_fasta, skipredundant_out_fasta, skipredundant_out_fasta_red, mode, threshold, minthreshold)
  print("\nDone filtering redundant sequences!\n")
  # get number of seqs in nr and redundant sets
  print("Number of non-redundant sequences to keep:")
  wc_cmd1 = "grep '^>' " + skipredundant_out_fasta + " | wc -l"
  os.system(wc_cmd1)
  print("Number of redundant sequences to be dropped:")
  wc_cmd2 = "grep '^>' " + skipredundant_out_fasta_red + " | wc -l"
  os.system(wc_cmd2)
  q_red_ok = input("Does this look ok? (y/n)").lower()
  if (q_red_ok == 'n'):
    print("\nExiting ... You may want to try again, setting less strict / no skipredundant thresholds ...")
    sys.exit()
  elif (q_red_ok == 'y'):
    print("Good. Using the kept sequences for multiple sequences alignment next ...\n")

################################## align sequences (clustalo) ######################################

# check if sequences have be filtered on the previous step:
if (q_red == 'n'): # skipredundant was not used
  # input file (unfiltered .fa file from search)
  co_in_fasta  = search_out + ".fa"
  # output file for aligned .fa file
  co_out_fasta = search_out + "_co_msa.fa"
  # run clustalo
  print("\nInitiating clustal omega multiple sequence alignment for all the " + str(seqs_count) + " protein sequences found ... \n") 
  fun.run_clustalo(co_in_fasta, co_out_fasta)
  print("Clustalo analysis complete!\n")
elif (q_red == 'y'): # skipredundant was used
  # input file (filtered .fa file from skipredundant)
  co_in_fasta = skipredundant_out_fasta
  # output file for aligned .fa file
  co_out_fasta = search_out + "_co_msa.fa"
  # run clustalo
  print("\nInitiating clustal omega multiple sequence alignment for the:") 
  os.system(wc_cmd1)
  print("filtered (non-redundant) protein sequences remaining ... \n")
  fun.run_clustalo(co_in_fasta, co_out_fasta)
  print("Clustalo analysis complete!\n")

################################## plot amino acid conservation (plotcon) ######################################

# plotcon input file (created by clustalo)
plotcon_in_fasta = search_out + "_co_msa.fa"
print("Initiating plotcon to plot conservation of a protein sequence alignment ... \n")

while True: # will run the fun.run_plotcon function until no errors produced (otherwise it would exit the script)
  try:
    fun.run_plotcon(plotcon_in_fasta)
  except:
    # some error giving arguement to plotcon 
    print("\nWarning! Please check your arguements for plotcon are correct. Starting again ...\n")
    continue
  else:
    # no errors, exit loop
    break

print("\nPlotcon analysis completed! Please close the firefox window to continue.\nGraph also saved in current directory\n")

#print("good for now")
#sys.exit()

################################## get alignment information (infoalign) ######################################

# infoalign -sequence pyruvate_dehydrogenase_ascomycete_fungi_co_msa.fa -outfile pyruvate_dehydrogenase_ascomycete_fungi_co_msa.infoalign -noweight -noname
print("Get basic statistics about the aligned sequences ...\nUsing the infoalign programme\n")
# input .fa alignment file (from clustalo)
infoalign_in_fasta = search_out + "_co_msa.fa"
# output table file (.infoalign)
infoalign_out = search_out + "_co_msa.infoalign"
# full infoalign command
full_infoalign_cmd = "infoalign -sequence " + infoalign_in_fasta + " -outfile " + infoalign_out + " -noweight -noname"
# run the infoalign programme
os.system(full_infoalign_cmd)

## pandas
# read table
df = pd.read_csv(infoalign_out, sep="\t")
# sort by ascending % Change (% of changed positions compared to the consensus sequence) 
df.sort_values('% Change', ascending=True, inplace=True)
# get a list of the sequences accession numbers, most conserved oredered first
accs = []
for index in df.index: # assession numbers are extracted from the df indeces 
  accs += [re.search(r'.*co_msa.fa:(.*)', index).group(1).rstrip(" ")]

# write ordered table to .tsv file
df_filename = search_out + "_co_msa.infoalign.sorted"
df.to_csv(df_filename, sep = "\t", header = True)
print("Alignment info table, with most conserved sequences on top, saved at " + df_filename + "\n")

################################ scann against PROSITE database motifs ######################################

# input file (same as in plotcon)
prosite_in_fasta = search_out + "_co_msa.fa"
print("\nInitiating analysis to scan for motifs in the PROSITE db\n")

#while True: # will run the fun.run_prosite function until no errors produced (otherwise it would exit the script)
#  try:
#    fun.run_plotcon(plotcon_in_fasta)
#  except:
#    # some error giving arguement to plotcon 
#    print("\nWarning! Please check your arguements for  are correct. Starting again ...\n")
#    continue
#  else:
#    # no errors, exit loop
#    break












