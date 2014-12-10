# q2oligo.py 

### Convert QIIME files into Oligotyping format

#### Written by James Meadow - Sept 15 2014

----------

#### If you are also using QIIME: 


This simple python script subsets QIIME-formatted files by taxonomic name. 

The resulting sequence files (single taxon fasta) can be used for Oligotyping analysis.   

The input files: 
    
* tax_assignment.txt file resulting from assign_taxonomy.py 
* otu_map.txt  file resulting from QIIME OTU clustering. 
    This has a numeric OTU ID followed by tab-separated
    sequence IDs. This will be subsetted to contain only 
    entries matching correct taxonomy. 
* Taxonomic name. For instance, could be 'Firmicutes'.
*In fact, if you try it with the tiny example files, you should use that.*
Resulting files will have this name as a prefix. 

usage: 

```
python q2oligo.py tax_assignment.txt otu_map.txt 'Firmicutes'
```


Results: 
  
* Firmicutes_taxonomy.txt = OTU IDs followed by GreenGenes taxonomy. 
* Firmicutes_otu_map.txt = OTU map with only seqs matching the name given. 

The resulting subsetted OTU map can then be used in a  
  QIIME command to make a new subsetted fasta file. 
  e.g.: 
  
```
filter_fasta.py -f seqs.fna -m Firmicutes_otu_map.txt -o Firmicutes.fasta
```
And then, since QIIME retains all of the sequence header information, use the `stripMeta.py` script to strip the extra metadata from the sequence header:

``` 
python stripMeta.py Firmicutes.fasta Firmicutes_stripped.fasta
```

Now the fasta file is ready to be used in the Oligotyping pipeline. 

------

#### Or use the script as standalone without QIIME: 


You can also pass a sequence file to this script (which is much slower than QIIME). 
The `q2oligo.py` can be used alone to run the entire conversion. 
The only reason to do this is if you don't have QIIME installed, or if your sequence file
is quite small (<1gb). 


usage: 

```
python q2oligo.py tax_assignment.txt otu_map.txt seqs.fna 'Firmicutes'
```


Results:

* Firmicutes_taxonomy.txt = OTU IDs followed by GreenGenes taxonomy.
* Firmicutes_otu_map.txt = OTU map with only seqs matching the name given.
* Firmictues.fasta = fasta sequence file containing only sequences matching these OTUs. 


-------

Any deviation from these 3 or 4 arguments, in the correct order, passed to 
`q2oligo.py` will fail and exit with directions. 


-------

#### Update November 28 2014

This script is now compatible with Open Reference OTU Picking. 

Two bugs were fixed: 

* Previously the script ignored OTU ID prefixes added during open reference OTU picking in QIIME. This was fixed, so that all OTUs are carried through the process, regardless of their prefix. 
* The old script assumed that all OTUs were found in the OTU map, but if used with a subset OTU map (such as an `mc2` default where singletons are removed), the script will now indicate a lower number of OTUs were written to the new taxon OTU map. 




