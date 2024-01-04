#!/usr/bin/env python3

import argparse
from os import path
from ete3 import Tree


#
# -----------------------------------------------------------------------------
# Return the overlap / intersection of two arrays
# -----------------------------------------------------------------------------
#
def intersection(a, b):
    return [e for e in a if e in b]


#
# -----------------------------------------------------------------------------
# Return the difference of two arrays
# -----------------------------------------------------------------------------
#
def diff(a, b):
    return [e for e in a if e not in b]


#
# -----------------------------------------------------------------------------
# read file content or from standard input
# -----------------------------------------------------------------------------
#
def read_input(input):
    if path.exists(input) == True:
        with open(input) as file:
            string = file.read() 
    else:
        string = input
    return string


#
# -----------------------------------------------------------------------------
# reformat FASTA headers
# -----------------------------------------------------------------------------
#
def reformat_fasta_headers(fasta_string):
    new_fasta = ""
    for line in fasta_string.split("\n"):
        if ">" in line:
            new_fasta += (line.split("/")[0]) + "\n"
        else:
            new_fasta += line + "\n"
    return new_fasta


#
# -----------------------------------------------------------------------------
# reformat LIST headers
# -----------------------------------------------------------------------------
#
def reformat_list_headers(fasta_string):
    new_fasta = ""
    for line in fasta_string.split("\n"):
        new_fasta += (line.split("/")[0]) + "\n"
    return new_fasta


#
# -----------------------------------------------------------------------------
# extract species names from FASTA string as list
# -----------------------------------------------------------------------------
#
def get_fasta_species(fasta_string):
    species_list = []
    for entry in fasta_string.split("\n"):
        if ">" in entry:
            species_list.append(entry[1:])
    return species_list


#
# -----------------------------------------------------------------------------
# tree with all species is pruned with species list
# -----------------------------------------------------------------------------
#
def prune(bigtree, species):
    tree = Tree(bigtree)
    tree.prune(species, preserve_branch_length = True)
    return str(tree.write(format = 9))


#
# -----------------------------------------------------------------------------
# Adapt fasta to species and maybe duplicates
# -----------------------------------------------------------------------------
#
def adapt_fasta(fasta_string, species, removeduplicates):
    new_fasta = ""
    dups = []
    print(fasta_string)
    if ">" in fasta_string:
        for entry in fasta_string.split("\n"):
            if len(entry) == 0:
                continue
            if entry[0] == ">":
                spec = entry[1:]
                if spec not in species:
                    skip = True
                elif removeduplicates == True and spec in dups:
                    skip = True
                else:
                    new_fasta += entry + "\n"
                    dups.append(spec)
                    skip = False
            elif skip == False:
                new_fasta += entry + "\n"
        if skip == False and len(entry) > 0:
            new_fasta += entry + "\n"
        return new_fasta
    else:
        for spec in fasta_string.split("\n"):
            if len(spec) == 0:
                continue
            if spec not in species:
                continue
            elif removeduplicates == True and spec in dups:
                continue
            else:
                new_fasta += spec + "\n"
                dups.append(spec)
        if len(spec) > 0:
            new_fasta += entry + "\n"
        return new_fasta
