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
def EC_in_fasta():
     '''
     -Parse the string representing a comment associated to an EC numbe
     -Parse EC number from the comment and save non duplicated 
     ones to a global variable
     -Parse UniProt accessions id using EC numbers
     -get the fasta record of the Uniprot ID, 
     -append the corresponding EC number to the header and save the fasta
          file in the local machine
        '''
     EC_final=[]
     print ('Brenda parser is starting')
     with BRENDAParser(brenda_flat) as parser:
          try:
                 brenda = parser.parse()
          except Exception as e:
                 print (str(e))
     
     ec_comment = [ec for ec in brenda if brenda[ec][0].comment is not None]
     for i in range(0,len(ec_comment)):
          ec=brenda[ec_comment[i]][0].comment#valid Ec number from the comment
          EC=re.findall(r'\bEC\s[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\b',ec)#regular expression to parse EC from comment
          for i in EC:
               if i not in EC_final:#remove duplicated EC numbers
                    EC_final.append(i)               
     print(str(len(EC_final)),'EC number were parsed.')
     if not os.path.isdir(fast_outputfolder):
              os.makedirs(fast_outputfolder)     
     print ('Extractin of uniprot identifiers and Fasta file modification')
     for e in EC_final:
          EC_number=e.split("EC ")[1]#string of ec_numbers to be used to find the protein identifier
          for prot_id in brenda[EC_number][0].proteins:
               protein = brenda[EC_number][0].proteins[prot_id]
               uniprot_id=protein.identifiers#list of uniprot identifiers
               if len(uniprot_id)!=0:#for one EC number we can have more than one id depending on the organism
                    try:  
                         for id in uniprot_id:
                              url_with_id = "%s%s%s" %(uniprot_url, id, ".fasta") 
                              file_from_uniprot =urlopen(url_with_id)
                              fasta=file_from_uniprot.readlines()
                              f=open(fast_output+'/'+e+'_'+id+'.fasta','w')
                              for line in fasta:
                                   line=line.decode('utf-8')#remove the Bytes literals,b', from lines 
                                   if 'SV=' in line:
                                      header=line.replace(line.strip(),line.strip()+' '+e.replace(' ','='))
                                      f.write(header)
                                   else:
                                      fasta_seq=line.strip()
                                      f.write(fasta_seq)
                              f.close()                             
                    except Exception as e:
                         print (str(e))
     print ('EC numbers are now added to Fasta headers')
if __name__ == "__main__":
     uniprot_url = "http://www.uniprot.org/uniprot/"  # constant Uniprot Namespace
     brenda_flat='brenda_download.txt'
     fast_output='EC_unip_fasta'
     print (EC_infasta())
