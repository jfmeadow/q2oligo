#!/bin/python


import sys
import os
import re



def getSequences(oldFastaName, newFastaName):

  print '\n...............................\n\
    Searching the sequence file for extra metadata\n...............................\n'

  fastaFile = open(oldFastaName, 'rU')
  fastaFileRead = fastaFile.read()
  fastaFileRead = fastaFileRead.split('>')

  newFasta = open(newFastaName, 'w')


  for line in fastaFileRead: 
    fileSeqID = re.search(r'\A(\S+)\s(.+)(\n.+)', line)
    if fileSeqID: 
      sequence = '>' + fileSeqID.group(1) + fileSeqID.group(3) + '\n'
      newFasta.write(sequence)

  print '\n...............................\n\
    Finished cleaning the sequence file\n...............................\n'      

  newFasta.close()
  fastaFile.close()

def main(): 

  # useage: python stripMeta.py Firmicutes.fasta Firmicutes_stripped.fasta
  getSequences(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
  main()
