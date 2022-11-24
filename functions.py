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
  
# get protein family, taxonomic group from user
def give_prot_taxon():
  protein = input("Write the protein family you want to search for:").lower()
  taxon   = input("Write the taxonomic group you want to search for:").lower()
  names = {"protein": protein, "taxon": taxon}
  return  names   
  
# 
