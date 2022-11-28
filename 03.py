#!/usr/bin/python3

# import modules
import os, subprocess, sys, re
#import pandas as pd

# import my functions 
import functions as fun

fasta = open(search_out_fasta, 'r')
seqs_count = 0     # counter for sequences
species_dict = {}  # dict to count no. of accurances for each species: species_dict = {species1: no of appearances,...} -> no of keys = no of species
for line in fasta:
  #line = line.rstrip("\n")    # read each line, strip '\n' at the end
  if re.search(r'^>', line.rstrip("\n")):  # get header lines (start with ">")
    line = line.rstrip("\n")
    #print(line)
    #header_line = line
    ## count no. of sequences  
    seqs_count += 1
    ## get species name 
    species = re.search(r'.*?\[(.*)].*', line).group(1)         # exract species name from header (inside square brackets) - use as key
    #print(species)
    species_dict[species] = species_dict.get(species,0) + 1     # if first time, set value of dict to 0 then add 1.+ 1 every time species seen again 
  else:
  #  print(line)

fasta.close()
######
#fasta = open(search_out_fasta, 'r')
#fasta.close()
with open(search_out_fasta) as fasta:
  fasta_contents = fasta.read()
  header = re.search(r'^>.*?\[.*\]\n', fasta_contents)
  print(header)





#>XP_001272711.1 pyruvate dehydrogenase [Aspergillus clavatus NRRL 1]\nMLSKSLRYRGSLRRMCPVLSCTDRRFMAQVADVRNIPTEDDKLFNVPLSEESFETYNFDPPPYTVDTTKR\nKLKDMYRDMLSIRRMESTGQEAVAVGIEHAITKEDKLITAYRSHGFTFMRGASIRSIVGELLGRQDGISH\nGKGGSMHMFLESFFGGNGIVGAHVPVGAGIAFAQQYNDGSNVTIDIYGDGAANQGQVYEAFNMAKLWNLP\nILFGCENNKYGMGTSAERASAITDYHKRGQYIPGLRVNGMDVLAVLAAMKHGKQFIQAGKGPLIYDLRER\nLIEWGIITEDEAKAMDKDVHGIINQEVAEAEKMTEPELRLDVLFEDVYARGSEPKQRRGRTLAETFY\n


q_win = input("Default window size for plotcon is 4.\n(Number of columns to average alignment quality over.)\nThe larger this value is, the smoother the plot will be.\nDo you want to change it? (y/n)")
try: 
   winsize = input("Give window size for plotcon. Default = 4:")
   
except ValueError : 
  "not an integer"
  
  





