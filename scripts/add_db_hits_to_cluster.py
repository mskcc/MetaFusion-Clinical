#!/usr/bin/env python
import sys
import pandas as pd
import numpy as np
import pygeneann_MetaFusion as pygeneann
import pybedtools.bedtool as bedtools
import itertools
import sequtils
import argparse
import re
import ast

#python add_db_hits_to_cluster.py /MetaFusion/RUNS/BT474.KPL4.MCF7.SKBR3.Aug-20-2020/final.cluster /MetaFusion/RUNS/BT474.KPL4.MCF7.SKBR3.Aug-20-2020/cluster.preds.collected.gencode_mapped.wAnnot.CANCER_FUSIONS

#PARSER
parser = argparse.ArgumentParser()
parser.add_argument('cluster', action='store', help='Fusion cluster file )')
parser.add_argument('db_hit_file', action='store', help='FusionAnnotator output file subsetted for cancer DB hits')
parser.add_argument('cluster_type', action='store', help='full or subset')
args = parser.parse_args()
#
##INPUTS
cluster_file_subset=args.cluster
db_hit_file = args.db_hit_file
cluster_type=args.cluster_type

#CREATE FUSION LIST
fusion_list = []
for line in open(cluster_file_subset, "r"):
    if line.startswith("#"):
        continue
    if cluster_type == "full":
        fusion = pygeneann.CategoryFusions(line)
    elif cluster_type == "subset":
        fusion = pygeneann.CategoryFusionSubset(line)
    else:
        raise ValueError('Invalid cluster type argument')
    fusion_list.append(fusion)
#category_stats = pygeneann.CategoryFusionStats(cluster)
sys.stderr.write("length of fusion list: " + str(len(fusion_list)) + "\n" )

# Read in "cluster.preds.collected.gencode_mapped.wAnnot.CANCER_FUSIONS" file
db_hit_lines=[line for line in open(db_hit_file, "r")]
db_hit_dict = {}
for line in db_hit_lines:
    #Extract databases which are hit
    line=line.split("\t")
    FIDs=line[7]
    hits=line[-1]
    start = hits.find("\"ATTS") 
    end = hits.find(']', start)
    hits = hits[start:end+1]
    hits = ast.literal_eval(hits.split(":")[1])
    #Populate dictionary
    db_hit_dict[FIDs] = hits
#pygeneann.output_cluster_header()
#for f in fusion_list: 
#  try:
#    FIDs=",".join(f.fusion_IDs)
#    db_hits =  db_hit_dict[FIDs] 
#    f.cancer_db_hits = db_hit_dict[FIDs]
#    f.out()
#  except:
#    f.out()
#Annotate .cluster file column "cancer_db_hits" with database hits 
if cluster_type == "full":
  # output header
  pygeneann.output_cluster_header()
  for f in fusion_list: 
    try:
      FIDs=",".join(f.fusion_IDs)
      db_hits =  db_hit_dict[FIDs] 
      f.cancer_db_hits = db_hit_dict[FIDs]
      f.out()
    except:
      f.out()
elif cluster_type == "subset":
  # output header
  pygeneann.output_cluster_header_subset()
  for f in fusion_list: 
    try:
      FIDs=",".join(f.fusion_IDs)
      db_hits =  db_hit_dict[FIDs] 
      f.cancer_db_hits = db_hit_dict[FIDs]
      f.out_subset()
    except:
      f.out_subset()
else:
    raise ValueError('Invalid cluster type argument')
