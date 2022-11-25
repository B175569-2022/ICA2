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
  protein = input("Write the protein family you want to search for:").lower()
  q1 = input("Do you want to use a taxonid or a taxonomic group name for your search? Press 1 for taxonid or 2 for taxonomic group name:") # returns str
  if (q1 == '1'):
    taxonid = input("Write the taxonid you want to search for:").lower()
    prot_taxon = {"protein": protein, "taxonid": taxonid}
    return  prot_taxon
  elif (q1 == '2'):
    taxon_name = input("Write the taxonomic group you want to search for:").lower()
    prot_taxon = {"protein": protein, "taxon_name": taxon_name}
    return  prot_taxon 
  else:
    return "Please try again giving correct input(1 for taxonid or 2 for taxonomic group name):"
# 
