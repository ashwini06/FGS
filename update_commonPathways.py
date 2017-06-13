#!/usr/bin/python -py

## Script to download the pathwaycommon9 and rearrange the file format and output the file rearrange_*
## Version: 


import os
import re
from glob import glob
import pdb
import urllib
import gzip

FGS_dir = "/home/proj/func/FGS_update";
#FGS_dir = "/Users/ashwini/Documents/Evinet/FGSupdate"

species_id = {'9606':'Homo_sapiens'}
print "Processing for {} to retrieve data from PathwayCommons9".format(species_id['9606'])
CPW_dir = os.path.join(FGS_dir, species_id['9606'],'PathwayCommons9')
if not os.path.isdir(CPW_dir):
    os.makedirs(CPW_dir)
os.chdir(CPW_dir)

urllib.urlretrieve("http://www.pathwaycommons.org/archives/PC2/v9/PathwayCommons9.All.hgnc.gmt.gz", "PathwayCommons9_All.hgnc.gz")
ofl = open("rearrange_PathwayCommons9.txt",'w')
with gzip.open('PathwayCommons9_All.hgnc.gz', 'rb') as ifl:
        for ln in iter(ifl):
                ln = ln.strip().split('\t')
                pwid = ln[0].split('/')[-1].replace(" ","")
                noids = re.compile('^Pathway_.*')
                tmp_info = {}
                for info in ln[1].split(';'):
                        info = info.split(':')
                        try:
                                tmp_info[info[0].strip()] = info[1].strip()
                        except:
                                pass
                pwnm = tmp_info.get('name','')
                if noids.match(pwid):
                        pwid=''
                        nm = pwnm
                else : 
                        pwid = pwid
                        nm = pwid+":"+pwnm
                source = tmp_info.get('datasource','')
                species = tmp_info.get('organism','')
                for gene in ln[2:]:
                        opLine = "\t".join([gene, nm, source, species_id.get(species, 'NA')]) + "\n"                
                        ofl.write(opLine)
#os.remove("PathwayCommons9_All.hgnc.gz")                        
print "Done: PathwayCommons9 file created for {}, output filename:{}".format(species_id['9606'], "rearrange_PathwayCommon9.txt")




