#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WEKO3_simple_loader.py ver 0.17b

usage: (you must setting mapping.txt befor use this script)
  python weko3_simple_loder.py -i input.tsv -m mapping.txt

  Output file name is "jsonheader_metadata.txt"
"""
import sys
import re
import argparse


def json_mapping(file):
    """
    カラム名とJSONパスのマッピング
    """
    colmn = {}
    map_dict = {}
    header_no = {}
    map_file = open(file, "r", encoding="utf-8")
    header_line = map_file.readline().rstrip("\n")
    i = 0
    for colmns in header_line.split("\t"):
        header_no[colmns] = i
        i += 1
    for line in map_file:
        colmns = line.rstrip("\n").split("\t")
        colmn = {}
        colmn["name"] = colmns[header_no["name"]]
        colmn["config"] = colmns[header_no["config"]]
        colmn["path1"] = colmns[header_no["path1"]]
        colmn["path2"] = colmns[header_no["path2"]]
        colmn["value"] = colmns[header_no["value"]]
        colmn["attrib1"] = colmns[header_no["attrib1"]]
        colmn["attrib2"] = colmns[header_no["attrib2"]]
        map_dict[colmn["name"]] = colmn
    return map_dict


def set_map_table(map_dict, header):
    """
    入力データ順にしたマッピング情報
    """
    i = 0
    for colmn in header.split("\t"):
        map_table.append(None)
        if colmn in map_dict:
            if map_dict[colmn]["value"]:
                map_table[i] = map_dict[colmn]
        else:
            print(colmn + " is ignored")
        i += 1


def make_header(map_table_row, sort1, sort2, sort3):
    """
    項目に応じたヘッダをセット
    """
    header_data = {}
    header_data["name"] = map_table_row["name"]
    header_data["config"] = map_table_row["config"]
    header_data["sort1"] = sort1
    header_data["sort2"] = sort2
    header_data["sort3"] = sort3
    return header_data


def set_data(data, value, multi, i, j):
    """
    値と属性をヘッダにセット
    """
    repeat_num = "."
    if multi == 1:
        repeat_num = '[' + str(j) + '].'
    if multi == 2:
        repeat_num = '[' + str(j) + ']'
        if map_table[i]["path2"]:
            repeat_num = repeat_num + '.'

    header_base = ""
    if map_table[i]["path1"]:
        header_base = map_table[i]["path1"] + repeat_num
    if map_table[i]["path2"]:
        header_base = header_base + map_table[i]["path2"]
        if multi == 1:
            header_base = header_base +  "."

    # value
    if multi == 2:
        header = header_base
    else:
        header = header_base + map_table[i]["value"]
    data[header] = value
    header_data = make_header(map_table[i], i, j, 0)
    headers[header] = header_data

    # attrib1
    if map_table[i]["attrib1"]:
        attrib = map_table[i]["attrib1"].split("=")
        attrib_n = attrib[0]
        attrib_v = attrib[1]
        attrib_v = re.sub(r'^\"', "", attrib_v)
        attrib_v = re.sub(r'\"$', "", attrib_v)
        header = header_base + attrib_n
        data[header] = attrib_v
        header_data = make_header(map_table[i], i, j, 1)
        headers[header] = header_data

    # attrib2
    if map_table[i]["attrib2"]:
        attrib = map_table[i]["attrib2"].split("=")
        attrib_n = attrib[0]
        attrib_v = attrib[1]
        attrib_v = re.sub(r'^\"', "", attrib_v)
        attrib_v = re.sub(r'\"$', "", attrib_v)
        header = header_base + attrib_n
        data[header] = attrib_v
        header_data = make_header(map_table[i], i, j, 2)
        headers[header] = header_data


def output_tsv(records, outfile):
    """
    WEKO3一括登録フォーマットTSVで出力
    """

    outfile = open(output, "w", encoding="utf-8")

    # Colmn Sort
    colmns = []
    colmns = sorted(
        headers,
        key=lambda x: (
          headers[x]['sort1'], headers[x]['sort2'], headers[x]['sort3']
        )
    )
    colmns = headers

    # First Line
    buffer = []
    for colmn in colmns:
        buffer.append(colmn)
    outfile.write("\t".join(buffer))
    outfile.write("\n")

    # Second Line
    buffer = []
    for colmn in colmns:
        buffer.append(headers[colmn]["name"])
    outfile.write("\t".join(buffer))
    outfile.write("\n")

    # rows
    for record in records:
        buffer = []
        for colmn in colmns:
            if colmn in record:
                buffer.append(record[colmn])
            else:
                buffer.append("")
        outfile.write("\t".join(buffer))
        outfile.write("\n")

    outfile.close()


def simple_loader(separator, mapping, input, output):
    """
    メインループ
    """
    infile = open(ARGS.input, "r", encoding="utf-8")

    # ヘッダ処理
    set_map_table(json_mapping(mapping), infile.readline().rstrip("\n"))

    records = []
    # 入力ファイルの各レコード処理
    for line in infile:
        if line:
            line = line.rstrip("\n")
            data = {}
            path_count = {}
            pre_repeat = 0
            i = 0
            for value in line.split("\t"):
                if not map_table[i] or not map_table[i]["value"] or not value:
                    i += 1
                    continue
                multi = 0
                if "Allow Multiple" in map_table[i]["config"]:
                    multi = 1
                if map_table[i]["value"] == "#":
                    multi = 2
                if multi == 0:
                    set_data(data, value, multi, i, 0)
                    pre_repeat = 0
                else:
                    path1_path2 = ""
                    if map_table[i]["path1"]:
                        path1_path2 = map_table[i]["path1"]
                    if map_table[i]["path2"]:
                        path1_path2 += "_" + map_table[i]["path2"]
                    splited_values = []
                    splited_values = value.split(separator)
                    match = re.search(r'^repeat\("(.*)"\)$', value)
                    if match is not None:
                        splited_values = [match.group(1)] * pre_repeat
                    pre_repeat = len(splited_values)
                    for splited_value in splited_values:
                        if path1_path2 in path_count:
                            path_count[path1_path2] += 1
                        else:
                            path_count[path1_path2] = 0
                        j = path_count[path1_path2]
                        set_data(data, splited_value, multi, i, j)
                i += 1
            records.append(data)
    infile.close()
    output_tsv(records, output)


if __name__ == '__main__':
    # Setting
    separator = '|'
    output = 'jsonheader_metadata.txt'

    # args
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input', type=str, required=True)
    parser.add_argument('-m', '--mapping', help='mapping', type=str, required=True)
    ARGS = parser.parse_args()

    # Global
    headers = {}
    map_table = []

    # Excute
    simple_loader(separator, ARGS.mapping, ARGS.input, output)
