#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import Logger
import Finder
import Output
import Extractor


def merge_ast_script(ast_script, ast_node_a, ast_node_b, mapping_ba):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    Output.normal("\t\tmerging AST script")
    merged_ast_script = list()
    inserted_node_list = list()
    deleted_node_list = list()
    # print(ast_script)
    for script_line in ast_script:
        # print(script_line)
        if "Insert" in script_line:
            node_id_a = int(((script_line.split(" into ")[0]).split("(")[1]).split(")")[0])
            node_id_b = int(((script_line.split(" into ")[1]).split("(")[1]).split(")")[0])
            if node_id_b not in inserted_node_list:
                merged_ast_script.append(script_line)
            inserted_node_list.append(node_id_a)
        elif "Delete" in script_line:
            node_id = int((script_line.split("(")[1]).split(")")[0])
            if node_id in deleted_node_list:
                continue
            node = Finder.search_ast_node_by_id(ast_node_a, node_id)
            child_id_list = Extractor.extract_child_id_list(node)
            deleted_node_list = deleted_node_list + child_id_list
            merged_ast_script.append(script_line)
        elif "Move" in script_line:
            move_position = int((script_line.split(" at ")[1]))
            move_node_str = (script_line.split(" into ")[0]).replace("Move ", "")
            move_node_id = int((move_node_str.split("(")[1]).split(")")[0])
            move_node = Finder.search_ast_node_by_id(ast_node_b, move_node_id)
            move_node_type = move_node['type']
            if move_node_type == "CaseStmt":
                continue
            target_node_id_b = int(((script_line.split(" into ")[1]).split("(")[1]).split(")")[0])
            if target_node_id_b in inserted_node_list:
                continue
            target_node_id_a = mapping_ba[target_node_id_b]
            target_node_a = Finder.search_ast_node_by_id(ast_node_a, target_node_id_a)
            replacing_node = target_node_a['children'][move_position]
            replacing_node_id = replacing_node['id']
            replacing_node_str = replacing_node['type'] + "(" + str(replacing_node['id']) + ")"
            script_line = "Replace " + replacing_node_str + " with " + move_node_str

            merged_ast_script.append(script_line)
            deleted_node_list.append(replacing_node_id)
            child_id_list = Extractor.extract_child_id_list(replacing_node)
            deleted_node_list = deleted_node_list + child_id_list
    return merged_ast_script


def filter_ast_script(ast_script, info_a, info_b, mapping_ba):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    Output.normal("\t\tfiltering AST script")
    source_path_a, line_range_a, ast_node_a = info_a
    source_path_b, line_range_b, ast_node_b = info_b
    filtered_ast_script = list()
    line_range_start_a, line_range_end_a = line_range_a
    line_range_start_b, line_range_end_b = line_range_b
    line_numbers_a = set(range(int(line_range_start_a), int(line_range_end_a) + 1))
    line_numbers_b = set(range(int(line_range_start_b), int(line_range_end_b) + 1))
    merged_ast_script = merge_ast_script(ast_script, ast_node_a, ast_node_b, mapping_ba)
    # print(merged_ast_script)
    for script_line in merged_ast_script:
        if "Insert" in script_line:
            node_id_b = int(((script_line.split(" into ")[0]).split("(")[1]).split(")")[0])
            node_b = Finder.search_ast_node_by_id(ast_node_b, node_id_b)
            node_type_b = node_b['type']
            node_line_start = int(node_b['start line'])
            node_line_end = int(node_b['end line']) + 1
            # if node_line_start in skip_lines:
            #     continue
            node_line_numbers = set(range(node_line_start, node_line_end))
            # print(node_line_numbers)
            intersection = line_numbers_b.intersection(node_line_numbers)
            if intersection:
                if node_type_b in ["IfStmt"]:
                    body_node = node_b['children'][1]
                    filtered_ast_script.append(script_line)
                    # count = 0
                    # for child_node in body_node['children']:
                    #     if int(child_node['start line']) not in skip_lines:
                    #         count = count + 1
                    # if count != 0:
                    #     filtered_ast_script.append(script_line)
                else:
                    filtered_ast_script.append(script_line)
        elif "Delete" in script_line:
            node_id_a = int((script_line.split("(")[1]).split(")")[0])
            node_a = Finder.search_ast_node_by_id(ast_node_a, node_id_a)
            node_line_start = int(node_a['start line'])
            node_line_end = int(node_a['end line']) + 1
            node_line_numbers = set(range(node_line_start, node_line_end))
            intersection = line_numbers_a.intersection(node_line_numbers)
            if intersection:
                filtered_ast_script.append(script_line)
        elif "Replace" in script_line:
            node_id_a = int(((script_line.split(" with ")[0]).split("(")[1]).split(")")[0])
            node_a = Finder.search_ast_node_by_id(ast_node_a, node_id_a)
            node_line_start = int(node_a['start line'])
            node_line_end = int(node_a['end line']) + 1
            node_line_numbers = set(range(node_line_start, node_line_end))
            intersection = line_numbers_a.intersection(node_line_numbers)
            if intersection:
                filtered_ast_script.append(script_line)
    # print(filtered_ast_script)
    return filtered_ast_script


def filter_ast_script_by_line(ast_script, info_a, info_b, mapping_ba, skip_lines):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    Output.normal("\t\tfiltering AST script")
    source_path_a, line_range_a, ast_node_a = info_a
    source_path_b, line_range_b, ast_node_b = info_b
    filtered_ast_script = list()
    line_range_start_a, line_range_end_a = line_range_a
    line_range_start_b, line_range_end_b = line_range_b
    line_numbers_a = set(range(int(line_range_start_a), int(line_range_end_a) + 1))
    line_numbers_b = set(range(int(line_range_start_b), int(line_range_end_b) + 1))
    # print(merged_ast_script)
    for script_line in ast_script:
        if "Insert" in script_line:
            node_id_b = int(((script_line.split(" into ")[0]).split("(")[1]).split(")")[0])
            node_b = Finder.search_ast_node_by_id(ast_node_b, node_id_b)
            node_type_b = node_b['type']
            node_line_start = int(node_b['start line'])
            node_line_end = int(node_b['end line']) + 1
            if node_line_start in skip_lines:
                continue
            node_line_numbers = set(range(node_line_start, node_line_end))
            intersection = line_numbers_b.intersection(node_line_numbers)
            if intersection:
                if node_type_b in ["IfStmt"]:
                    body_node = node_b['children'][1]
                    count = 0
                    for child_node in body_node['children']:
                        if int(child_node['start line']) not in skip_lines:
                            count = count + 1
                    if count != 0:
                        filtered_ast_script.append(script_line)
                else:
                    filtered_ast_script.append(script_line)
    return filtered_ast_script