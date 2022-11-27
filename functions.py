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
  ##
  # run command
  os.system(full_clustalo_cmd)
  return "\nSequence alignment saved at: " + co_out_fasta



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
  print("Your plotcon options: " + full_plotcon_cmd)
  # test if new options are valid
  if (graph in ("ps", "hpgl", "hp7470", "hp7580", "meta", "cps", "x11", "tek", "tekt", "none", "data", "xterm", "png", "gif", "pdf", "svg") and (winsize > 0) and isinstance(winsize,int)):
    #print("Your plotcon options: " + full_plotcon_cmd)
    pass
  else:
    sys.exit("Your new options are not right. Please try again using the correct formats.")
  # run plotcon if all goods 
  os.system(full_plotcon_cmd)
  # display graph in firefox browser 
  firefox_cmd = "firefox plotcon." + graph
  os.system(firefox_cmd)
  return 


  
  
  







