"""
This script adds EC numbers from Brenda enzyme data base to the header of the 
corresponding protein fasta file in the Uniprot.
Version: 1.0 (May 2019)
Author: Sondes kalboussi
"""
import sys,os,re
sys.path.insert(0, 'BRENDA-Parser')
from urllib.request import urlopen
from brenda.parser import BRENDAParser
import collections

def EC_infasta():
     '''
     -Parse the string representing EC number
     -Parse UniProt accessions id using EC numbers
     -get the fasta of the Uniprot ID, 
     -append the corresponding EC number to the header and save the fasta
          file in the local machine
        '''    
     print ('Brenda parser is starting')
     with BRENDAParser(brenda_flat) as parser:
          try:
                 brenda = parser.parse()
          except Exception as e:
                 print (str(e))     
     EC_number= [ec for ec in brenda]            
     print (str(len(EC_number)),'EC number were parsed.')
     if not os.path.isdir(fast_output):
              os.makedirs(fast_output)     
     print ('Extraction of uniprot identifiers and fasta modification')   
     Uniprot_EC={}#dic key is EC and value is uniprot id
     for e in EC_number:
          for prot_id in brenda[e][0].proteins:
               protein = brenda[e][0].proteins[prot_id]
               uniprot_id=protein.identifiers#list of uniprot identifiers
               if len(uniprot_id)!=0:
                    EC='EC= '+e
                    Uniprot_EC[EC]=uniprot_id
     Multi_EC= collections.defaultdict(list)# reversed dic with key is uniprot id and value is list of EC number(s) if exist.
     for key,value in Uniprot_EC.items():
         for i in value:
            Multi_EC[i].append(key)
     for n,m in Multi_EC.items():
          try:
                url_with_id = "%s%s%s" %(uniprot_url,n, ".fasta") 
                file_from_uniprot =urlopen(url_with_id)
                fasta=file_from_uniprot.readlines()
                f=open(fast_output+'\'+n+'.fasta','w+')
                for line in fasta:
                    line=line.strip().decode('utf-8')
                    if line.startswith('>'):
                        if len(m)>1:                                            
                            #print(n,' has multiple EC number'): add this line to see the uniprot id with multiple Ec number
                            header= line.replace(line,line+' '+' '.join([j for j in m]))  
                            f.write('%s\n' % (header))
                        else: 
                            header=line.replace(line,line+' '+''.join(m))
                            f.write('%s\n' % (header))
                    else:
                           fasta_seq=line.strip()
                           f.write('%s\n' %(fasta_seq))
                f.close()                     
                                 
          except Exception as error:
                 print (str(error))

     return ('EC numbers are now added to Fasta headers')                  
if __name__ == "__main__":
     uniprot_url = "http://www.uniprot.org/uniprot/"  # constant Uniprot Namespace
     brenda_flat='brenda_download.txt'
     fast_output='EC_unip_fasta'
print (EC_infasta())
