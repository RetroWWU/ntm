#!/usr/bin/env python3

import argparse
import sys
from os import path
from ete3 import Tree
from NTM_Functions import *

#--------------------------------------------------------------------------------
# INPUT
#--------------------------------------------------------------------------------

parser = argparse.ArgumentParser()

required_args = parser.add_argument_group('required arguments')
required_args.add_argument("-t","--tree", help = "path to newick file or newick tree string", required = True)
required_args.add_argument("-f","--fasta", help = "path to fasta file or fasta string", required = True)

parser.add_argument("-n","--name", help = "name of output files")
parser.add_argument("-d","--dir", help = "path to output directory", default = "./")
parser.add_argument("--acro", action = "store_true", default = False, help = "rename species names to acronyms (e.g. Homo_sapiens -> hom_sap)")
parser.add_argument("--ctl", action = "store_true", default = False, help = "create CTL file for paPAML")
parser.add_argument("--rmd", action = "store_true", default = False, help = "remove duplicate headers from FASTA")

args = parser.parse_args()
tree_input = args.tree
fasta_input = args.fasta
name = args.name
dir = args.dir
acro = args.acro
ctl = args.ctl
removeduplicates = args.rmd

#--------------------------------------------------------------------------------
# TREE
#--------------------------------------------------------------------------------

tree_string = read_input(tree_input)

try:
    tree = Tree(tree_string)
except:
    print("ERROR: Tree not readable by ete3.", file = sys.stderr)
    exit(1)
    
#--------------------------------------------------------------------------------
# REFORMAT FASTA
#--------------------------------------------------------------------------------

fasta_string = read_input(fasta_input)

if ">" in fasta_string:
    fasta_string = reformat_fasta_headers(fasta_string)
else:
    fasta_string = reformat_list_headers(fasta_string)

#--------------------------------------------------------------------------------
# SPECIES LIST
#--------------------------------------------------------------------------------

if ">" in fasta_string:
    species_list = get_fasta_species(fasta_string)
else:
    species_list = fasta_string.split("\n")
    species_list = [string for string in species_list if string != ""] #v1.2

#--------------------------------------------------------------------------------
# MARK / REMOVE DUPLICATES
#--------------------------------------------------------------------------------

if len(set(species_list)) < len(species_list):
    if removeduplicates == False:
        print("WARNING: There are duplicate FASTA headers. Consider to remove them for paPAML input.")

#--------------------------------------------------------------------------------
# Adjust species_list to newick tree leaves
#--------------------------------------------------------------------------------

names = tree.get_leaf_names()
species_diff = diff(species_list, names)
species_list = intersection(names, species_list)
if not species_list:
    print("ERROR: There is no valid species or sequence given!", file = sys.stderr)
    exit(1)
fasta_string = adapt_fasta(fasta_string, species_list, removeduplicates)

#--------------------------------------------------------------------------------
# PRUNE TREE
#--------------------------------------------------------------------------------

pruned_tree = prune(bigtree = tree_string, species = species_list)

#--------------------------------------------------------------------------------
# ACRO
#--------------------------------------------------------------------------------

acronyms = {}
for species in species_list:
    acronym = ""
    for i in species.split("_"):
        acronym += i[0:3] + "_"
    acronyms[species] = acronym[:-1].lower()

if acro == True:
    for acronym in acronyms:
        pruned_tree = pruned_tree.replace(acronym, acronyms[acronym])
        fasta_string = fasta_string.replace(acronym, acronyms[acronym])

#--------------------------------------------------------------------------------
# OUTPUT FILES
#--------------------------------------------------------------------------------

if name == None:
    output_fasta = "seqfile.fasta"
    output_tree = "treefile.tre"
    output_ctl = "paPAML.ctl"
    output_diff = "species.diff"
else:
    output_fasta = name + ".fasta"
    output_tree = name + ".tre"
    output_ctl = name + ".ctl"
    output_diff = name + ".diff"

if ctl == True:
    ctl_text = "seqfile = "+output_fasta + "\ntreefile = " + output_tree
    with open(dir + output_ctl, "w") as file:
        file.write(ctl_text)

with open(dir + output_fasta, "w") as file:
    file.write(fasta_string)

with open(dir + output_tree, "w") as file:
    file.write(pruned_tree)

with open(dir + output_diff, "w") as file:
    file.write(",".join(species_diff))
    