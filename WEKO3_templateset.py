#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WEKO3_templeteset.py ver 0.06b

usage: (Inputfile name is defiend "jsonheader_metadata.txt")
    python weko3_templateet.py -t template.txt -o output.tsv
"""

import argparse

if __name__ == '__main__':

    # input file name
    INFILE_NAME = "jsonheader_metadata.txt"

    # args
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--template', help='template', type=str, required=True)
    parser.add_argument('-o', '--output', help='output', type=str, required=True)
    ARGS = parser.parse_args()

    # Read Template
    tempalatefile = open(ARGS.template, "r", encoding="utf-8")
    line_01 = tempalatefile.readline()
    line_02 = tempalatefile.readline()
    line_03 = tempalatefile.readline()
    line_04 = tempalatefile.readline()
    line_05 = tempalatefile.readline()
    tempalatefile.close()
    template_table = {}

    i = 0
    for colmn in line_02.rstrip("\n").split("\t"):
        template_table[colmn] = i
        i += 1

    # template & Input File header matting
    infile = open(INFILE_NAME, "r", encoding="utf-8")
    header = infile.readline().rstrip("\n")  # First Line
    infile.readline()  # Second line Skip
    point = [None] * len(header.split("\t"))
    j = 0
    for colmn in header.split("\t"):
        if colmn in template_table:
            point[j] = template_table[colmn]
        else:
            print(colmn + " is invalid")
        j += 1

    # Read value & Output
    outfile = open(ARGS.output, "w", encoding="utf-8")
    outfile.write(line_01)
    outfile.write(line_02)
    outfile.write(line_03)
    outfile.write(line_04)
    outfile.write(line_05)
    for record in infile:
        record = record.rstrip("\n")
        line = [""] * i
        k = 0
        for value in record.split("\t"):
            if not point[k] == None:
                line[point[k]] = value
            k += 1
        outfile.write("\t".join(line))
        outfile.write("\n")

    infile.close()
    outfile.close()
