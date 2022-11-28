#!/usr/bin/python3

# import modules
import os, subprocess, sys, re
import pandas as pd

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

# run skipredundant
def run_skipredundant(skipredundant_in_fasta, skipredundant_out_fasta, skipredundant_out_fasta_red, mode=1, threshold=90.0, minthreshold=20.0, gapopen=10.0, gapextend=0.5):
  # write full command. options: -in seqs, mode, up threshold, (lower threshold), gapopen, gapextend, out seqs to keep, out seqs not to include
  # if set mode=2, a lower threshold will be used too
  if (mode == 1):
    full_skipredundant_cmd = "skipredundant -sequences " + skipredundant_in_fasta + " -mode " + str(mode) + " -threshold " + str(threshold) + " -gapopen " + str(gapopen) + " -gapextend " + str(gapextend) + " -outseq " + skipredundant_out_fasta + " -redundantoutseq " + skipredundant_out_fasta_red
    print("full skipredundant command is:\n" + full_skipredundant_cmd + "\n")
    os.system(full_skipredundant_cmd)
    return
  elif (mode == 2):
    full_skipredundant_cmd = "skipredundant -sequences " + skipredundant_in_fasta + " -mode " + str(mode) + " -maxthreshold " + str(threshold) + " -minthreshold " + str(minthreshold) + " -gapopen " + str(gapopen) + " -gapextend " + str(gapextend) + " -outseq " + skipredundant_out_fasta + " -redundantoutseq " + skipredundant_out_fasta_red
    print("full skipredundant command is:\n" + full_skipredundant_cmd + "\n")
    os.system(full_skipredundant_cmd)
    return
  else:
    return "Error, seems that mode was not set properly (1 or 2)"

# run clustalo
def run_clustalo(co_in_fasta, co_out_fasta):  
#clustalo -i my-in-seqs.fa -o my-out-seqs.fa -v
  # input name (.fa file from search)
  #co_in_fasta  = search_out + ".fa"
  # output name for aligned .fa file
  #co_out_fasta = search_out + "_co_msa.fa" 
  # clustalo options: --force to overwrite existing output
  full_clustalo_cmd = "clustalo -i " + co_in_fasta + " -o " + co_out_fasta + " -v --force"
  # run command
  os.system(full_clustalo_cmd)
  return "\nSequence alignment saved at: " + co_out_fasta

# run plotcon
def run_plotcon(plotcon_in_fasta, winsize = 4, graph = 'pdf'): # arguement as input file for plotcon
  # ask winsize
  q_win = input("Default window size for plotcon is 4.\n(Number of columns to average alignment quality over.)\nThe larger this value is, the smoother the plot will be.\nDo you want to change it? (y/n)").lower()
  if (q_win == 'y'):
    winsize = int(input("Please give you new window size:"))
  elif (q_win == 'n'):
    print("winsize remains 4")
  else: 
    print("Did not understand the answer. Default winsize remains.")
  # ask output format
  q_out = input("Default output graph is 'pdf'. Do you want to change that? (y/n)").lower()
  if (q_out == 'y'):
    graph = input("Please choose your new graph type (ps, hpgl, hp7470, hp7580, meta, cps, x11, tek, tekt, none, data, xterm, png, gif, pdf, svg):")
  elif (q_out == 'n'):
    print("Output graph type remains pdf")
  else: 
    print("Did not understand the answer. Default graph type remains.")
  # full plotcon command
  full_plotcon_cmd = "plotcon -sequences " + plotcon_in_fasta + " -winsize " + str(winsize) + " -graph "  + str(graph)
  print("Your plotcon options:\n" + full_plotcon_cmd)
  # test if new options are valid
  if (graph in ("ps", "hpgl", "hp7470", "hp7580", "meta", "cps", "x11", "tek", "tekt", "none", "data", "xterm", "png", "gif", "pdf", "svg") and (winsize > 0) and isinstance(winsize,int)):
    #print("Your plotcon options: " + full_plotcon_cmd)
    pass
  else:
    sys.exit("Your new options are not right. Please try again using the correct formats.")
  # run plotcon if all goods 
  os.system(full_plotcon_cmd)
  # display graph in firefox browser 
  firefox_cmd = "firefox plotcon*" + graph
  print("Running a firefox window to dispaly the graph. Please close the window to continue.")
  os.system(firefox_cmd)
  return 

# run prosite scan
#def run_prosite_scan(prosite_in_fasta):
  
  


