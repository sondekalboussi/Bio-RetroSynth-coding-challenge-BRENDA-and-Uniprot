
import sys,os
import re
from urllib.request import urlopen
sys.path.insert(0, 'BRENDA-Parser')
from brenda.parser import BRENDAParser
uniprot_url = "http://www.uniprot.org/uniprot/"  # constant Uniprot Namespace
EC_final=[]#list of unique ec numbers from flat file
#Parse information from Brenda database
#def get_EC_uniprot_id():
with BRENDAParser('brenda_download.txt') as parser:
        try:
            brenda = parser.parse()
        except Exception as e:
            print (str(e))
    #Parse EC numbers
ec_comment = [ec for ec in brenda if brenda[ec][0].comment is not None]
for i in range(0,len(ec_comment)):
            old_ec=brenda[ec_comment[i]][0].ec_number#old ec number
            ec=brenda[ec_comment[i]][0].comment#valid Ec number from the comment
            EC=re.findall(r'\bEC\s[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\b',ec)#regular expression to parse EC from comment
            for i in EC:
                if i not in EC_final:#remove duplicated EC numbers
                        EC_final.append(i)
if not os.path.isdir("Uniprot_fast"):
    os.makedirs("Uniprot_fast")
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
                            f=open('Uniprot_fast\\'+e+'_'+id+'.fasta','w')
                            for line in fasta:
                                line=line.decode('utf-8') 
                                if 'SV=' in line:
                                    header=line.replace(line.strip(),line.strip()+' '+e.replace(' ','='))
                                    f.write(header)
                                else:
                                    fasta_seq=line.strip()
                                    f.write(fasta_seq)
                            f.close()
                    except Exception as e:
                                    print ('verify the following EC number',e)
