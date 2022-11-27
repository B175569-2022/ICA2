#!/usr/bin/python3

# import modules
import os, subprocess, sys, re
#import pandas as pd

# import my functions 
import functions as fun

search_out = "pyruvate_dehydrogenase_ascomycete_fungi"

plotcon_in_fasta = search_out + "_co_msa.fa"
print("Initiating plotcon to plot conservation of a protein sequence alignment ... \n")

while True:
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
