#!/usr/bin/python -py

## Script to download KEGG pathways from KEGG database
# http://rest.kegg.jp/list/pathway/$organism
# Version : http://rest.kegg.jp/info/pathway


import os
import urllib
import pdb
import re


FGS_dir = "/home/proj/func/FGS_update"
#FGS_dir = "/Users/ashwini/Documents/Evinet/FGSupdate"

species = {'mmu': 'Mus_musculus', 'hsa': 'Homo_sapiens', 'rno': 'Rattus_norvegicus', 
			'ath': 'Arabidopsis_thaliana', 'dme': 'Drosophila_melanogaster',
			'cel': 'Caenorhabditis_elegans','sce': 'Saccharomyces_cerevisiae'}
for org in species.keys():
	print "Processing for {} to retrieve KEGG pathways".format(species[org])
	kegg_dir = os.path.join(FGS_dir, species[org], "KEGG")
	if not os.path.isdir(kegg_dir):
		os.makedirs(kegg_dir)
	os.chdir(kegg_dir)
	urllib.urlretrieve ("http://rest.kegg.jp/list/{}".format(org),"KEGG_gene_anno_{}.txt".format(org))
	anno_info = {}
	with open("KEGG_gene_anno_{}.txt".format(org), 'r') as geneanno_fl:
		for anno in iter(geneanno_fl):
			matchobj = re.search(".*uncharacterized.*",anno)
			if not matchobj:	
				gid, desc = anno.strip().split('\t')
				gnm = desc.split("|")[1].split(';')[0].replace(' (RefSeq) ','').split(',')[0]
				anno_info[gid] = gnm
	#os.remove("KEGG_gene_anno_{}.txt".format(org))

	urllib.urlretrieve ("http://rest.kegg.jp/list/pathway/{}".format(org),"KEGG_Pathway_{}.txt".format(org))
	kegg_info = {}
	with open("KEGG_Pathway_{}.txt".format(org), 'r') as ifl, open("rearrange_KEGGpathway.txt",'w') as ofl:
		for ln in iter(ifl):
			try:
				pwid,pwnm = ln.strip().split("\t")
				pwid = pwid.replace('path:','')
				pwinfo = pwnm.split(' - ')
				pwnm = "_".join(pwinfo[:-1]).strip().replace(" ","_")
				pwnm = pwid+":"+ pwnm
				species_nm = pwinfo[-1].strip().split("(",1)[0].strip().replace(" ","_")
				kegg_info[pwid] = pwnm
				urllib.urlretrieve ("http://rest.kegg.jp/link/genes/{}".format(pwid),"KEGG_pwids_tmp.txt")
				with open ("KEGG_pwids_tmp.txt") as tmp_fl:
					for tid in iter(tmp_fl):
						tid, gid = tid.strip().split("\t")
						tid = tid.replace("path:","")
						ofl.write("\t".join([anno_info[gid], pwnm, "KEGG", species_nm]) + "\n")

			except:
				pass
			#	os.remove("KEGG_pwids_tmp.txt")
	#os.remove("KEGG_Pathway_{}.txt".format(org))
	print "Done: KEGG file created for {}, output filename:{}".format(species[org], "rearrange_KEGGpathway.txt")

















