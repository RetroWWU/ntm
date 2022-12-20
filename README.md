![NTM logo](https://github.com/RetroWWU/ntm/blob/main/ntm_logo.tiff)

# Description

NewickTreeModifier (NTM) is a tool to prune a reference Newick tree to selected species by using the ete3 package. It is especially useful for paPAML users, as it creates all necessary paPAML input files by unifying the provided tree and sequences and creating a corresponding CTL file.

# Installation

NTM is implemented in Python3 which needs to be installed by the user.
Package dependencies are os (https://docs.python.org/3/library/os.html), argparse (https://docs.python.org/3/library/argparse.html) and ete3 (http://etetoolkit.org/download/).

# Conda
```zsh
conda create -n ntm
conda activate ntm
[...]
```

# Usage
```zsh
NTM.py [-h] -t TREE -f FASTA [-n NAME] [-d DIR] [--acro] [--ctl] [--rmd]
```
## Required arguments
```zsh
-t TREE, --tree TREE  	path to newick file or newick tree string
-f FASTA, --fasta FASTA	path to fasta file or fasta string
```
## Optional arguments
```zsh
-h, --help            	show this help message and exit
-n NAME, --name NAME  	name of output files
-d DIR, --dir DIR     	path to output directory
--acro                	rename species names to acronyms (e.g. Homo_sapiens → hom_sap)
--ctl                 	create CTL file for paPAML
--rmd                 	remove duplicate headers from FASTA
```

More details are available in our publication.

