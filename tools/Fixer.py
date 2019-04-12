#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import sys, os
from common.Utilities import execute_command, error_exit, show_partial_diff, backup_file
from common import Definitions
from ast import ASTGenerator
import Logger
import Finder
import Emitter


FILE_SYNTAX_ERRORS = ""
FILENAME_BACKUP = "backup-syntax-fix"


def extract_return_node(ast_node, line_number):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    node_type = str(ast_node["type"])
    return_node_list = list()
    if node_type == "ReturnStmt":
        return_node_list.append(ast_node)
        return return_node_list
    else:
        if len(ast_node['children']) > 0:
            for child_node in ast_node['children']:
                return_node_list += extract_return_node(child_node, line_number)

    if node_type == "FunctionDecl":
        for return_node in return_node_list:
            start_line = int(return_node['start line'])
            end_line = int(return_node['end line'])
            # print(start_line, line_number, end_line)
            if start_line <= line_number <= end_line:
                return return_node
    else:
        return return_node_list


def replace_code(patch_code, source_path, line_number):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    content = ""
    if os.path.exists(source_path):
        with open(source_path, 'r') as source_file:
            content = source_file.readlines()
            content[line_number-1] = patch_code

    with open(source_path, 'w') as source_file:
        source_file.writelines(content)


def fix_return_type(source_file, source_location):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    Emitter.normal("\t\tfixing return type")
    line_number = int(source_location.split(":")[1])
    ast_map = ASTGenerator.get_ast_json(source_file)
    function_node = Finder.search_function_node_by_loc(ast_map, int(line_number), source_file)
    return_node = extract_return_node(function_node, line_number)
    function_definition = function_node['value']
    function_name = function_node['identifier']
    function_return_type = (function_definition.replace(function_name, "")).split("(")[1]
    start_line = return_node['start line']
    end_line = return_node['end line']
    original_statement = ""
    if function_return_type.strip() == "void":
        new_statement = "return;\n"
        backup_file(source_file, FILENAME_BACKUP)
        replace_code(new_statement, source_file, start_line)
        backup_file_path = Definitions.DIRECTORY_BACKUP + "/" + FILENAME_BACKUP
        show_partial_diff(backup_file_path, source_file)
    elif function_return_type.strip() == "int":
        new_statement = "return -1;\n"
        backup_file(source_file, FILENAME_BACKUP)
        replace_code(new_statement, source_file, start_line)
        backup_file_path = Definitions.DIRECTORY_BACKUP + "/" + FILENAME_BACKUP
        show_partial_diff(backup_file_path, source_file)
    else:
        error_exit("NEW RETURN TYPE!")
    # check_syntax_errors()


def fix_syntax_errors(source_file):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    Emitter.normal("\t\tfixing syntax errors")
    with open(FILE_SYNTAX_ERRORS, 'r') as error_log:
        read_line = error_log.readline()
        source_location = read_line.split(": ")[0]
        error_type = (read_line.split(" [")[-1]).replace("]", "")
        if "return-type" in error_type:
            fix_return_type(source_file, source_location)


def check_syntax_errors(modified_source_list):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    Emitter.sub_sub_title("computing syntax errors")
    for source_file in modified_source_list:
        Emitter.normal("\t" + source_file)
        Emitter.normal("\t\tchecking syntax errors")
        check_command = "clang-check -analyze " + source_file + " > " + FILE_SYNTAX_ERRORS
        check_command += " 2>&1"
        ret_code = int(execute_command(check_command))
        if ret_code != 0:
            fix_syntax_errors(source_file)
        else:
            Emitter.normal("\tno syntax errors")


def set_values():
    global FILE_SYNTAX_ERRORS
    FILE_SYNTAX_ERRORS = Definitions.DIRECTORY_OUTPUT + "/syntax-errors"


def check(modified_source_list):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    set_values()
    check_syntax_errors(modified_source_list)
