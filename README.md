# Classifying and plotting fold change values of RNAseq data obatined from the metascape software analysis

In this project, I write a Python program called `metascape.py` that accepts a list of positional arguments that are metascape generated Excel files and output csv file. Metascape provides the understanding of the multiple gene analysis compared with the library of known gene pools and their predicted protein networks.

The first positional argument, `file1.xlsx`, contains the data of the fold change of the genes. The file must have two columns named '_ensembl_gene_id_' and '_FoldChange_'. Metascape generates this '_ensembl_gene_id_' corresponding to the genes obtained from the RNA sequences. If the value of the '_FoldChange_' is equal or greater than 1.2, the genes are classified as upregulated; otherwise the genes are classified as downregulated. The program should show an error if the `file1.xlsx` does not contain the required columns.

The second positional argument, `file2.xlsx`, contains the data of the LogP of the predicted pathways of the corrsponding genes. The '_LogP_' values denotes the randomness of obtained fold changes. The more negative LogP value is, there is less chance of the fold change to become random. The file should have two sheets named '_Annotation_' and '_Enrichment_'. '_Annotation_' sheet must have two columns with '_Input ID_' and '_Gene ID_' where '_Input ID_' matches with the '_ensembl_gene_id_' in the `file1.xlsx`. '_Enrichment_' sheet must have columns named '_GroupID_', '_Term_', '_Description_', '_LogP_', and '_Genes_'. '_Genes_' in the '_Enrichment_' sheet matches with the '_Gene ID_' in the '_Annotation_' sheet. Only the summaries in the '_GroupID_' are used for the pathway classification. '_Genes_' involved in the same pathway are described in the '_Description_' column and annotated with specific '_Term_'. 

The third positional argumnet, `outfile.csv`, should contain the summary dataframe compiling the columns of '_Pathway_' ('_Term_'+'_Description_'), '_LogP_', and '_Decision_' of the fold changes denoted as **up_reg** or **down_reg**. The file should also show the summary of the '_Gene_', '_ensemble_ID_', and '_FoldChange_'. 

Finally, the program should generate two plots based on the '_Decision_', one for '_up_reg_' and another for '_down_reg_', of the summary dataframe as .png format. The X-axis of the plots should show the -LogP values and the Y-axis should show the corresponding '_Pathway_'.

When run with no arguments, the program should print a brief usage statement:

```
$ ./metascape.py
usage: metascape.py [-h] file1.xlsx file2.xlsx outfile.csv
metascape.py: error: the following arguments are required: file1.xlsx, file2.xlsx, outfile.csv
```

When run with the `-h|--help` flag, it should print a more detailed help message:

```
$ ./metascape.py -h
usage: metascape.py [-h] file1.xlsx file2.xlsx outfile.csv

Fold change of RNAseq data

positional arguments:
  file1.xlsx   Input file with fold change
  file2.xlsx   Input file with LogP and geneID
  outfile.csv  Output file name

optional arguments:
  -h, --help   show this help message and exit
 ```

The program should reject a bad input file:

```
$ ./metascape.py foo blargh baz
usage: metascape.py [-h] file1.xlsx file2.xlsx outfile.csv
metascape.py: error: file1 "foo" must be an excel file
```

The program should reject a bad output file type:
```
$ ./metascape.py ./inputs/foldchange.xlsx ./inputs/enrichment.xlsx baz
usage: metascape.py [-h] file1.xlsx file2.xlsx outfile.csv
metascape.py: error: outfile "baz" must be a csv file
```

The program should reject file2.xlsx containing wrong sheet names:

```
$ ./metascape.py ./inputs/foldchange.xlsx ./inputs/wrong_input.xlsx out.csv
usage: metascape.py [-h] file1.xlsx file2.xlsx outfile.csv
metascape.py: error: file2 "./inputs/wrong_input.xlsx" does not contain required sheets.
```

The program should reject file2.xlsx containing wrong column names:

```
$ ./metascape.py ./inputs/foldchange.xlsx ./inputs/wrong_columns.xlsx out.csv
usage: metascape.py [-h] file1.xlsx file2.xlsx outfile.csv
metascape.py: error: file2 "./inputs/wrong_columns.xlsx" does not contain required columns.
```

The program should reject file1.xlsx containing wrong column names:

```
$ ./metascape.py ./inputs/wrong_columns.xlsx ./inputs/enrichment.xlsx out.csv
usage: metascape.py [-h] file1.xlsx file2.xlsx outfile.csv
metascape.py: error: file1 "./inputs/wrong_columns.xlsx" does not contain required columns.
```

When run with valid input files, the program should write summary dataframe in the `<outfile>` and plot LogP values in the `up_reg.png` and `down_reg.png` files corresponding to their fold change values.
The program should finish with a message of where the output was written:

```
$ ./metascape.py ./inputs/foldchange.xlsx ./inputs/enrichment.xlsx out.csv
See summary in "out.csv"
See plots in "up_reg.png" and "down_reg.png" files.
```

A passing test suite looks like the following:

```
$ make test
pytest -v --pylint --flake8 test.py metascape.py
=========================================================== test session starts ===========================================================
...
collected 10 items                                                                                                                        

test.py::PYLINT SKIPPED (file(s) previously passed pylint checks)                                                                   [ 10%]
test.py::FLAKE8 SKIPPED (file(s) previously passed FLAKE8 checks)                                                                   [ 20%]
test.py::test_exists PASSED                                                                                                         [ 30%]
test.py::test_usage PASSED                                                                                                          [ 40%]
test.py::test_bad_outfile PASSED                                                                                                    [ 50%]
test.py::test_bad_inputfile1 PASSED                                                                                                 [ 60%]
test.py::test_bad_inputfile2 PASSED                                                                                                 [ 70%]
test.py::test1 PASSED                                                                                                               [ 80%]
metascape.py::PYLINT SKIPPED (file(s) previously passed pylint checks)                                                              [ 90%]
metascape.py::FLAKE8 SKIPPED (file(s) previously passed FLAKE8 checks)                                                              [100%]

====================================================== 6 passed, 4 skipped in 10.10s ======================================================
```

## Author

Samina Momtaz <saminamomtaz@email.arizona.edu>
