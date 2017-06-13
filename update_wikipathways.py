#!/usr/bin/python -py

## Script to download the pathwaycommon9 and rearrange the file format and output the file rearrange_*
## Version : http://data.wikipathways.org/20170510/gmt/ (dates in filenames)


import os
import re
import gzip
import pdb
import urllib

FGS_dir = "/home/proj/func/FGS_update"
#FGS_dir = "/Users/ashwini/Documents/Evinet/FGSupdate"

urllib.urlretrieve ("ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz","gene_info.gz")
print "Download gene_info file to {}".format(FGS_dir)
gene_info = {}
with gzip.open('gene_info.gz', 'rb') as gfl:
	for glines in iter(gfl):
		glines = glines.strip().split('\t')
		try:
			gene_info[glines[1]] = glines[2]
		except:
			pass

os.remove("gene_info.gz")
for org in ["Mus_musculus", "Homo_sapiens", "Rattus_norvegicus", "Arabidopsis_thaliana", 
			"Caenorhabditis_elegans", "Drosophila_melanogaster", "Saccharomyces_cerevisiae" ]:
	print "Processing for {} to retrieve WikiPathways".format(org)
	dir_nm = os.path.join(FGS_dir,org,"{}".format("WikiPathways"))
	if not os.path.isdir(dir_nm):
		os.makedirs(dir_nm)
	os.chdir(dir_nm)

	urllib.urlretrieve ("http://data.wikipathways.org/20170510/gmt/wikipathways-20170510-gmt-{}.gmt".format(org), "WikiPathways_{}.txt".format(org))
	with open("WikiPathways_{}.txt".format(org), 'r') as ifl, open("rearrange_wikipathway.txt",'w') as ofl:
		for ln in iter(ifl):
			ln = ln.strip().split('\t')
			pwnm = ln[0].split("%")[0].replace(" ","_")
			pwid = ln[1].split("/")[-1]
			for gid in ln[2:]:
				ofl.write("\t".join([gene_info.get(gid, gid), "{}:{}".format(pwid, pwnm), "WikiPathways", org]) + "\n")
	#os.remove("WikiPathways_{}.txt".fomat(org))
	print "Done: WikiPathways file created for {}, output filename:{}".format(org,"rearrange_wikipathway.txt")
		
