#!/usr/bin/env python3

# pylint: disable=too-many-arguments
"""
Author : saminamomtaz <saminamomtaz@localhost>
Date   : 2021-11-28
Purpose: Fold change of RNAseq data
"""

import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Fold change of RNAseq data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('foldchange',
                        metavar='file1.xlsx',
                        help='Input file with fold change')
    parser.add_argument('enrichment',
                        metavar='file2.xlsx',
                        help='Input file with LogP and geneID')
    parser.add_argument('outfile',
                        metavar='outfile.csv',
                        help='Output file name')

    args = parser.parse_args()

    # check file type
    if not args.foldchange.endswith('.xlsx'):
        parser.error(f'file1 "{args.foldchange}" must be an excel file')
    elif not args.enrichment.endswith('.xlsx'):
        parser.error(f'file2 "{args.enrichment}" must be an excel file')
    elif not args.outfile.endswith('.csv'):
        parser.error(f'outfile "{args.outfile}" must be a csv file')

    # check correctly formatted sheets
    # get the sheet names from args.enrichment file
    sheet_names_enrichment = list(pd.read_excel(args.enrichment, None).keys())
    if sheet_names_enrichment != ['Annotation', 'Enrichment']:
        parser.error(f'file2 "{args.enrichment}" does not contain required sheets.')
    else:
        # read the raw datas from metascape Sheet 'Annotation'
        args.annotation_all = pd.read_excel(args.enrichment, sheet_name='Annotation')
        # read the raw datas from metascape Sheet 'Enrichment'
        args.enrichment_all = pd.read_excel(args.enrichment, sheet_name='Enrichment')

    # read the raw datas from fold change file
    args.fold_change_all = pd.read_excel(args.foldchange)

    # check correctly formatted columns
    if not set(['Input ID', 'Gene ID']).issubset(args.annotation_all.columns):
        parser.error(f'file2 "{args.enrichment}" does not contain required columns.')
    elif not set(['GroupID', 'Term', 'Description', 'LogP', 'Genes']).issubset(args.enrichment_all.columns):
        parser.error(f'file2 "{args.enrichment}" does not contain required columns.')
    elif not set(['ensembl_gene_id', 'FoldChange']).issubset(args.fold_change_all.columns):
        parser.error(f'file1 "{args.foldchange}" does not contain required columns.')

    return args


# --------------------------------------------------
def create_summary(annotation_all, enrichment_all, fold_change_all):
    """Create a summary dataframe"""

    # extract the 'summary' rows from the 'Enrichment' sheet
    enrichment_selected = enrichment_all.loc[enrichment_all['GroupID'].str.contains("Summary")]

    # create summary dataframe
    plot_label = []
    val_LogP = []
    gene_list = []
    gene_1st = []
    ensum_list = []
    fold_list = []
    decision_list = []
    for ii in range(len(enrichment_selected)):
        plot_label += [enrichment_selected['Term'].iloc[ii] + ': ' + enrichment_selected['Description'].iloc[ii]]
        val_LogP += [enrichment_selected['LogP'].iloc[ii]]
        gene_list += [enrichment_selected['Genes'].iloc[ii].split(',')]
        # choosing the 1st gene from the gene list
        # as all genes have similar fold change
        gene_1st += [gene_list[ii][0]]

        # find out the 'ensemble_gene_id' corresponding
        # to the first gene of the 'gene_list' column
        for jj in range(len(annotation_all)):
            if gene_1st[ii] == annotation_all['Gene ID'].iloc[jj]:
                ensum_list += [annotation_all['Input ID'].iloc[jj]]
                break

        # find out the fold change corresponding to the 'ensemble_gene_id'
        for jj in range(len(fold_change_all)):
            if ensum_list[ii] == fold_change_all['ensembl_gene_id'].iloc[jj]:
                fold_list += [fold_change_all['FoldChange'].iloc[jj]]

                # if fold change is less than 1.2 define
                # as down_reg and else define it as up_reg
                if fold_list[ii] < 1.2:
                    decision_list += ['down_reg']
                else:
                    decision_list += ['up_reg']
                break

    # define summary dataframe
    summary_df = pd.DataFrame(list(zip(plot_label, val_LogP, gene_list, ensum_list, fold_list, decision_list)),
                              columns=['Pathway', 'LogP', 'Gene', 'ensemble_ID', 'FoldChange', 'Decision'])

    return summary_df


# --------------------------------------------------
def plot_fig(df, xlimit_right, figure_name):  # pylint: disable=too-many-arguments
    """
    function for plotting logP values

    Function description:
    df: dataframe containing the values of the logP and pathways
        df must have columns with the name 'LogP' and 'Pathway'
    xlimit_right: maximum value of the x axis in the plot
    figure_name: name of the saved figure

    Function usage:
    plot_fig(df,5,'file.png')

    """

    plt.figure(figsize=(20, 20))
    sns.barplot(-df.LogP, df.Pathway)  # pylint: disable=too-many-arguments
    plt.xlabel("-logP", fontsize=20)
    plt.xlim(right=xlimit_right)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.ylabel('', fontsize=20)
    plt.savefig(figure_name, bbox_inches='tight')


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    annotation_all = args.annotation_all
    enrichment_all = args.enrichment_all
    fold_change_all = args.fold_change_all

    # create summary dataframe
    summary_df = create_summary(annotation_all, enrichment_all, fold_change_all)

    # creating up and down regulation dataframe based on the
    # decision column from the summary dataframe
    up_df = summary_df[summary_df["Decision"] == 'up_reg']
    down_df = summary_df[summary_df["Decision"] == 'down_reg']

    # defining max x limit
    max_x_plot = np.ceil(max(-summary_df['LogP']) / 5) * 5

    # plotting up regulations
    plot_fig(up_df, max_x_plot, 'up_reg.png')

    # plotting down regulations
    plot_fig(down_df, max_x_plot, 'down_reg.png')

    # creating output file from the summary
    summary_df.to_csv(args.outfile)
    print(f"See summary in \"{args.outfile}\"")
    print('See plots in \"up_reg.png\" and \"down_reg.png\" files.')


# --------------------------------------------------
if __name__ == '__main__':
    main()
