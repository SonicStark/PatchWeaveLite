#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from tools import Logger


def write_var_map(var_map, output_file):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    content = ""
    for var in var_map:
        content += var + ":" + var_map[var] + "\n"
    with open(output_file, 'w') as map_file:
        map_file.writelines(content)


def write_skip_list(skip_list, output_file):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    content = "0\n"
    for line_number in skip_list:
        content += str(line_number) +  "\n"
    with open(output_file, 'w') as map_file:
        map_file.writelines(content)


def output_ast_script(ast_script, output_file):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    with open(output_file, 'w') as script_file:
        script_file.writelines(ast_script)