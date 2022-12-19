#!/usr/bin/env python3

import argparse
from os import path
from ete3 import Tree

'''
read file content or from standard input
'''
def read_input(input):
    if path.exists(input) == True:
        with open(input) as file:
            string = file.read() 
    else:
        string = input
    return string

'''
reformat FASTA headers
'''
def reformat_fasta_headers(fasta_string):

    new_fasta = ""

    for line in fasta_string.split("\n"):
        if ">" in line:
            new_fasta += (line.split("/")[0]) + "\n"
        else:
            new_fasta += line + "\n"
        
    return new_fasta

'''
reformat LIST headers
'''
def reformat_list_headers(fasta_string):

    new_fasta = ""

    for line in fasta_string.split("\n"):
        new_fasta += (line.split("/")[0]) + "\n"
        
    return new_fasta

'''
extract species names from FASTA file as list
'''
def get_fasta_species(fasta_path,format=0):
    
    species_list = []
    with open(fasta_path,"r") as fasta:
        for line in fasta:
            if ">" in line:
                species_list.append(line[1:-1])
        
    return species_list

'''
extract species names from FASTA string as list
'''
def get_fasta_species(fasta_string):
    
    species_list = []
    for entry in fasta_string.split("\n"):
        if ">" in entry:
            species_list.append(entry[1:])
        
    return species_list

'''
tree with all species is pruned with species list
package: ete3
'''
def prune(bigtree,species):
    
    from ete3 import Tree
    
    tree = Tree(bigtree)
    tree.prune(species, preserve_branch_length=True)
    
    return str(tree.write(format=9))

'''
remove sequences with duplicate headers
'''
def remove_duplicates(fasta_string):
    new_fasta = ""
    headers = []
    for entry in fasta_string.split("\n"):
        if ">" in entry and entry not in headers:
            new_fasta += entry + "\n"
            headers.append(entry)
            suppress_entry = False
        elif ">" in entry and entry in headers:
            suppress_entry = True
        elif ">" not in entry and suppress_entry == False:
            new_fasta += entry + "\n"
    
    return new_fasta
