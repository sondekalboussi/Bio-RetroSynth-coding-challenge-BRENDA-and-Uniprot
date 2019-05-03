# Bio-RetroSynth-coding-challenge-BRENDA-and-Uniprot
For every EC number listed in the BRENDA database, retrieve all the Uniprot accessions associated to the EC number in FASTA format. The corresponding EC number(s) from BRENDA must be present in the FASTA header.
The starting point of this code is a project improved by Alexandra-zaharia https://github.com/alexandra-zaharia/BRENDA-Parser, Brenda Parser is used to Parse the string representing a comment associated to an EC numbe, Using this EC number we extraxt UniProt accessions identifiers, get the fasta record of the Uniprot ID, append the corresponding EC number to the header and save the fasta file in the local machine. 

PS: Some EC numbers are mentioned are new EC but they are now longer in the DB such as EC 1.3.1.193
Some EC numbers have many uniprot id so more tha one fasta file depending on the corresponding organism
# BRENDA
The BRENDA database is the most important repository on enzyme activity and enzyme
ligands. Website: https://www.brenda-enzymes.org/
BRENDA proposes free and subscription-based programmatic access to enzyme data. The
free version comes in the form of a flat file (subjected to acceptance of the licence
agreement) available here:
https://www.brenda-enzymes.org/download_brenda_without_registration.php
BRENDA associates enzyme activity information (provided by EC numbers, EC 6.6.1.2 for
instance) with sequence information (provided by accession number, P29929 for instance).
The BRENDA flat file may be parsed with BRENDA-Parser:
https://github.com/alexandra-zaharia/BRENDA-Parser
# Uniprot
Protein sequences are available in Uniprot in FASTA format (among other formats).
For example, the FASTA header for accession P29929 is the following:

>sp|P29929|COBN_SINSX Aerobic cobaltochelatase subunit CobN
OS=Sinorhizobium sp. OX=42445 GN=cobN PE=1 SV=1

# Challenge
We wish to modify the FASTA header such that it contains EC number information; in the
case of P29929 it should be associated to EC 6.6.1.2. The FASTA header should therefore
read:

>sp|P29929|COBN_SINSX Aerobic cobaltochelatase subunit CobN
OS=Sinorhizobium sp. OX=42445 GN=cobN PE=1 SV=1 EC=6.6.1.2
