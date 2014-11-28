#!/bin/python

'''

Script to subset a QIIME OTU map by taxonomic name. 

Written by James Meadow (jfmeadow at gmail dot com)
Date: Sept 12 2014
  

The input files: 
    
  tax_assignment.txt file resulting from assign_taxonomy.py 
    
  otu_map.txt  file resulting from QIIME OTU clustering. 
    This has a numeric OTU ID followed by tab-separated
    sequence IDs. This will be subsetted to contain only 
    entries matching correct taxonomy. 
      
  Taxonomic name. For instance, could be 'Staphylococcus'
    Resulting files will have this name as a prefix. 

usage: python q2oligo.py tax_assignment.txt otu_map.txt 'Staphylococcus'

Results: 
  
  Staphylococcus_taxonomy.txt = OTU IDs followed by GreenGenes taxonomy. 
  Staphylococcus_otu_map.txt = OTU map with only seqs matching the name given. 

The resulting subsetted OTU map can then be used by 
  QIIME command to make a new subsetted fasta file. 
  e.g.: filter.fasta.py -f seqs.fna -m Staphylococcus_otu_map.txt -o Staphylococcus_sequences.fasta

'''

import sys
import os
import re
# import itertools


def SearchTax(taxAssFile, String): 
  
  print '\n...............................\n\
    Searching the taxonomy file\n...............................\n'
  # open, read files and split them by line
  f = open(taxAssFile, 'rU')   
  fRead = f.read()
  fRead = fRead.split('\n')

  numLines = len(fRead)

  # create lists to populate with data
  IDToFind = []
  IDMatched = []

  # loop through map looking for taxon pattern String
  for i in range(numLines):
    line = fRead[i]
    IDfind = re.search(String, line)

    # put IDs and taxa strings into list when they are found.
    if IDfind:
      otuID = re.search(r'\A(\S+)\t(.+)', line)  # added \A and \S to catch open ref prefix
      IDToFind.append(otuID.group(1))
      IDMatched.append(otuID.group(2))
  
  # create new file to write taxonomy. Name it same as search. 
  IDsOut = String + '_taxonomy.txt'
  # print IDsOut
  TaxIDsOut = open(IDsOut, 'w')
  
  # Write file. 
  for i in range(len(IDToFind)):
    TaxIDsOut.write(IDToFind[i] + '\t' + IDMatched[i] + '\n')


  # check output. 
  # print '\n------\n'
  # for ID in IDToFind: 
  #   print ID  
  # print '\n------\n'
  # for IDM in IDMatched:
  #   print IDM
  # print '\n------\n'
  
  # return list of OTUs to find in OTU map.   
  print '\n...............................\n\
    Finished searching the taxonomy file\n\
    Found ' + str(len(IDToFind)) + ' OTUs matching "' + String + \
    '"\n...............................\n'
  return IDToFind




def SearchOTUs(IDToFind, OTUsFile, String):  
  
  print '\n...............................\n\
    Searching the OTU map\n\
    This might take a minute\n...............................\n'

  # get list of IDs
  # IDToWrite is a list of numeric IDs

  # open otus.txt
  otuMap = open(OTUsFile, 'rU')
  otuMapRead = otuMap.read()
  otuMapRead = otuMapRead.split('\n')

  # how many in loop
  numLines = len(otuMapRead)

  # create new file to write taxonomy. Name it same as search. 
  IDsOut = String + '_otu_map.txt'
  # print IDsOut + '\n-----\n'

  SeqIDsOut = open(IDsOut, 'w')
  

  # loop twice - once over ID names and then over OTU map. 
  # Find each OTU ID and then add OTU ID and sequence IDs to dict. 
  IDwritten = 0   # new index in case some OTUs were not found. 
  for ID in IDToFind:
    for i in range(numLines):
      line = otuMapRead[i]
      IDfind = re.search(r'\A' + ID + '\t', line)
      if IDfind:
        SeqIDsOut.write(line + '\n')
        IDwritten = IDwritten + 1

  SeqIDsOut.close()      
  print '\n...............................\n\
    Finished searching the OTU map\n\
    Found ' + str(IDwritten) + ' OTUs and wrote them to ' + \
    IDsOut + '\n...............................\n'



def getSequences(fasta, String):

  print '\n...............................\n\
    Searching the sequence file\n\
    Good time to get coffee\n...............................\n'
  # find OTU map just created
  otuMapName = String + '_otu_map.txt'
  otuMap = open(otuMapName, 'rU')
  otuMapRead = otuMap.read()
  otuMapRead = otuMapRead.split('\n')

  fastaFile = open(fasta, 'rU')
  fastaFileRead = fastaFile.read()
  fastaFileRead = fastaFileRead.split('>')

  newFastaName = String + '.fasta'
  newFasta = open(newFastaName, 'w')

  seqList = []

  for line in otuMapRead: 
    eachOTU = re.search(r'\A(\d+)\t(.+)', line)
    if eachOTU: 
      seqIDs = eachOTU.group(2)
      checkTabs = re.search('\t', seqIDs)
      if checkTabs: 
        seqIDs = seqIDs.split('\t')
        for ID in seqIDs: 
          seqList.append(ID)
      else: 
        seqList.append(seqIDs)

  # print '\n\nmade it out of seqList.....\n\n'
  
  # pull out seqID from fasta line. 
  for line in fastaFileRead: 
    fileSeqID = re.search(r'\A(\S+)\s(.+)(\n.+)', line)
    if fileSeqID: 
      if fileSeqID.group(1) in seqList: 
        # sequence = '>' + line
        sequence = '>' + fileSeqID.group(1) + fileSeqID.group(3) + '\n'
        newFasta.write(sequence)

  print '\n...............................\n\
    Finished searching the sequence file\n\
    Found ' + str(len(seqList)) + ' sequences and wrote them to ' + \
    newFastaName + '\n...............................\n'      

  newFasta.close()


def main(): 

  # give directions if all args not satisfied. 
  if len(sys.argv) < 4:
    print '\n-------------------------------------------------\n'
    print '\nThis script will subset QIIME-formatted files by \n\
      any taxonomic level for oligotyping analysis. \n'

    print '\nYou have a choice of whether to use QIIME (faster) or \n\
      just use this script (slower) to make a new fasta file. \n\n'

    print 'If you use QIIME, this script needs 3 arguments: \n\
      * a taxonomy assignment text file, in QIIME format,\n\
      * an OTU map, also in QIIME format,\n\
      * and a taxonomy string in quotes, such as "Staphylococcus". \n\
      \n\
      example: \n\
        python q2oligo.py tax_assignments.txt otu_map.txt "Staphylococcus"\n\n\
      Then use QIIME thusly: \n\
        filter_fasta.py -f seqs.fna -m Staphylococcus_otu_map.txt -o Staphylococcus.fasta\n\n\
      And then to strip the extra metadata from the sequence header, use the other script in this folder: \n\
        python stripMeta.py Staphylococcus.fasta Staphylococcus_stripped.fasta\n\n'

    print 'However, if you don\'t mind waiting, it needs 4 things: \n\
      * a taxonomy assignment text file, in QIIME format,\n\
      * an OTU map, also in QIIME format,\n\
      * a fasta sequence file with labels that match the OTU map,\n\
      * and a taxonomy string in quotes, such as "Staphylococcus". \n\
      \n\
      example: \n\
        python q2oligo.py tax_assignments.txt otu_map.txt seqs.fna "Staphylococcus"\n\n'
    print '\n-------------------------------------------------\n'

    sys.exit(1)

  if len(sys.argv) == 4:
    IDToFind = SearchTax(sys.argv[1], sys.argv[3])
    SearchOTUs(IDToFind, sys.argv[2], sys.argv[3])
    # getSequences(sys.argv[3], sys.argv[4])

  if len(sys.argv) == 5:
    IDToFind = SearchTax(sys.argv[1], sys.argv[4])
    SearchOTUs(IDToFind, sys.argv[2], sys.argv[4])
    getSequences(sys.argv[3], sys.argv[4])


if __name__ == '__main__':
  main()
     





# python q2oligo.py tax_assignments.txt otus.txt seqs.fna 'Corynebacterium' 
# macqiime 
# filter_fasta.py -f seqs.fna -m Corynebacterium_otu_map.txt -o Corynebacterium.fasta
