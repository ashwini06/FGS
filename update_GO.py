#!/usr/bin/python -py


## Script to download GO terms from go database
## Version : http://geneontology.org/ontology/go.obo (first 2 lines)
## GO org code : http://www.geneontology.org/gene-associations/go_annotation_metadata.all.json

## File1
# MGI     MGI:1918911     0610005C13Rik           GO:0003674      MGI:MGI:2156816|GO_REF:0000015  ND
 #             F       RIKEN cDNA 0610005C13 gene              gene    taxon:10090     20100209        MGI

## File2
#[Term]
#id: GO:0000001
#name: mitochondrion inheritance
#namespace: biological_process

import os
import urllib
import gzip
import re
from collections import defaultdict
import pdb

FGS_dir = "/home/proj/func/FGS_update"
#FGS_dir = "/Users/ashwini/Documents/Evinet/FGSupdate"


species = {"mgi" : "Mus_musculus", "goa_human" : "Homo_sapiens", "rgd" : "Rattus_norvegicus",
			 "tair" : "Arabidopsis_thaliana", "fb" : "Drosophila_melanogaster", 
			 "wb" : "Caenorhabditis_elegans", "sgd" : "Saccharomyces_cerevisiae"}
for org in species.keys():
	print "Processing for {} to retrieve information from GO database".format(species[org])
	go_dir = os.path.join(FGS_dir,species[org],"{}".format("GO"))
	if not os.path.isdir(go_dir):
		os.makedirs(go_dir)
	os.chdir(go_dir)
	
	if org == "goa_human":
		urllib.urlretrieve ("http://geneontology.org/gene-associations/{}.gaf.gz".format(org),"GO_gene_association_{}.gz".format(org))
	else:
		urllib.urlretrieve ("http://geneontology.org/gene-associations/gene_association.{}.gz".format(org),"GO_gene_association_{}.gz".format(org))

	goid_info = defaultdict(list) 
	with gzip.open("GO_gene_association_{}.gz".format(org), 'rb') as ifl:
		for lines in iter(ifl):
			lines = lines.strip()
			if lines.startswith('!'):
				continue
			lines = lines.split('\t')
			goid_info[lines[4]].append({'gname':lines[2], 'mgi':lines[1]})
	
	op_BP = open("rearrange_GO_BP_{}.txt".format(species[org]), 'w')
	op_MF = open("rearrange_GO_MF_{}.txt".format(species[org]), 'w')
	op_CC = open("rearrange_GO_CC_{}.txt".format(species[org]), 'w')
	op_all = open("rearrange_GO_All_{}.txt".format(species[org]), 'w')		
	
	urllib.urlretrieve ("http://purl.obolibrary.org/obo/go.obo","go.obo")
	with open("go.obo", 'r') as obo_fl:
		tmp_obo = {} 
		keys_needed = ['id', 'name', 'namespace']
		for obo_ln in iter(obo_fl):
			obo_ln = obo_ln.strip()
			if re.search('^\[.*\]$', obo_ln):
				if not tmp_obo:
					continue
				goid = tmp_obo['id']
				name = tmp_obo['name'].replace(" ","_")
				nspace = tmp_obo['namespace']
				go_genes = goid_info.get(goid)
				if go_genes:
					processed_gene = []
					for gn in go_genes:
						gid = gn['gname']
						mgi = gn['mgi']
						if not gid in processed_gene:
							if (nspace == "biological_process" or nspace == "biological_process" or nspace == "cellular_component"):
								op_all.write("\t".join([gid, "{}:{}".format(goid, name), 
											 "GO:{}".format(nspace), species[org], mgi])+"\n")
								#processed_gene.append(gid)
							if nspace == "biological_process":
								op_BP.write("\t".join([gid, "{}:{}".format(goid, name), 
											 "GO:{}".format(nspace), species[org], mgi])+"\n")
								#processed_gene.append(gid)
							if nspace == "molecular_function":
								op_MF.write("\t".join([gid, "{}:{}".format(goid, name), 
											 "GO:{}".format(nspace), species[org], mgi])+"\n")
								#processed_gene.append(gid)
							if nspace == "cellular_component":
								op_CC.write("\t".join([gid, "{}:{}".format(goid, name), 
											 "GO:{}".format(nspace), species[org], mgi])+"\n")
							processed_gene.append(gid)

				tmp_obo = {}
				#else:
				#	print "\t".join(['NA', "{}:{}".format(goid, name), 
				#					 nspace, org, 'NA'])
			else: 
				try:
					k,v = obo_ln.split(":",1)
					if k in keys_needed:
						tmp_obo[k] = v.strip()
				except:
					pass
	print "Done: GO files created for {}".format(species[org])








