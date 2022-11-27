#!/usr/bin/python3

# modules
import os
import subprocess


# ask for directory to output files
def give_dir():
  dir = os.getcwd()
  ans = input("Do you wanto to use current directory for analysis? (y/n)").lower()
  if (ans == "n"):
    dir = input("Write here the full directory you want for the analysis:")
    os.chdir(dir)
    return "Working directory changed to " + dir
  return "Working directoty remained at " + dir
  
# get protein family, taxonomic group / taxonid from user
# returns dict with keys according to input: "taxon_name" or "taxonid"
def give_prot_taxon():
  protein = input("Write the protein family you want to search for:")
  q1 = input("Do you want to use a taxonid or a taxonomic group name for your search? Press 1 for taxonid or 2 for taxonomic group name:") # returns str
  if (q1 == '1'):
    taxonid = input("Write the taxonid you want to search for:")
    prot_taxon = {"protein": protein, "taxonid": taxonid}
    return  prot_taxon
  elif (q1 == '2'):
    taxon_name = input("Write the taxonomic group you want to search for:")
    prot_taxon = {"protein": protein, "taxon_name": taxon_name}
    return  prot_taxon 
  else:
    return "Please try again giving correct input(1 for taxonid or 2 for taxonomic group name):"


# run clustalo
def run_clustalo(search_out):  # search_out from 01.py
#clustalo -i my-in-seqs.fa -o my-out-seqs.fa -v
  # input name (.fa file from search)
  co_in_fasta  = search_out + ".fa"
  # output name for aligned .fa file
  co_out_fasta = search_out + "_co_msa.fa" 
  # clustalo options: --force to overwrite existing output
  full_clustalo_cmd = "clustalo -i " + co_in_fasta + " -o " + co_out_fasta + " -v --force"
  # ask if user wants a max sequence legnth ???
  os.system(full_clustalo_cmd)


#if (input("Do you want a max sequence length? (y/n)").lower() == "y"):
#    while True:
#      try:
#        maxseqlen = int(input("Please give you max sequence length: "))
#        full_clustalo_cmd_maxseqlen = "clustalo -i " + co_in_fasta + " -o " + co_out_fasta + " -v --force --maxseqlen=" + str(maxseqlen)
#        try:
#          os.system(full_clustalo_cmd_maxseqlen)
#        except:
#          print("clustalo error")
#      except ValueError: # if not given a number in input()
#        print("Sorry, Not a valid input. Try again.")
#        continue #Return to the start of the loop
#      else:
#        break 
# 









