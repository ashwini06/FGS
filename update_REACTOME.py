#!/usr/bin/python -py


# Script to download reactome patways from http://www.reactome.org/download/current/ReactomePathways.gmt.zip

# version :http://www.reactome.org/download/current/ (check for dates)


import os
import urllib
import gzip
import zipfile
import pdb
import re

FGS_dir = "/home/proj/func/FGS_update"
species = {"hsa": "Homo_sapiens"}
for org in ["hsa"]:
	print "Processing for {} to retrieve ReactomePathways".format(species[org])
	dir_nm = os.path.join(FGS_dir,species[org],"{}".format("REACTOME"))
	if not os.path.isdir(dir_nm):
		os.makedirs(dir_nm)
	os.chdir(dir_nm)
	


	urllib.urlretrieve ("http://www.reactome.org/download/current/ReactomePathways.gmt.zip","ReactomePathways.gmt.zip")
	op_fl = open("rearrange_ReactomePathways_{}.txt".format(species[org]), 'w')
	z = zipfile.ZipFile('ReactomePathways.gmt.zip', 'r')
	rfl = z.open(z.namelist()[0], 'r')
	for rlines in iter(rfl):
		rlines = rlines.strip().split('\t')
		pwnm = rlines[0].replace(" ","_")
		pwid = rlines[1]
		source = rlines[2]
		for gid in rlines[3:]:
			op_fl.write("\t".join([gid, "{}:{}".format(pwid,pwnm), source, species[org]])+ "\n")

	print "Done: Reactome Pathways file created for {}, output filename:rearrange_ReactomePathways_{}.txt".format(species[org],species[org])
