#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import sys

sys.path.append('./ast/')
import time
from common.Utilities import error_exit
from common import Definitions, Values
from ast import ASTGenerator
from tools import Mapper, Logger, Filter, Emitter, Differ

FILE_EXCLUDED_EXTENSIONS = ""
FILE_EXCLUDED_EXTENSIONS_A = ""
FILE_EXCLUDED_EXTENSIONS_B = ""
FILE_DIFF_C = ""
FILE_DIFF_H = ""
FILE_DIFF_ALL = ""
FILE_AST_SCRIPT = ""
FILE_AST_DIFF_ERROR = ""

diff_info = dict()


def analyse_source_diff():
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    global diff_info
    Differ.diff_files(Definitions.FILE_DIFF_ALL,
                      Definitions.FILE_DIFF_C,
                      Definitions.FILE_DIFF_H,
                      Definitions.FILE_EXCLUDED_EXTENSIONS_A,
                      Definitions.FILE_EXCLUDED_EXTENSIONS_B,
                      Definitions.FILE_EXCLUDED_EXTENSIONS,
                      Values.PATH_A,
                      Values.PATH_B)
    Emitter.sub_sub_title("analysing header files")
    Differ.diff_h_files(Definitions.FILE_DIFF_H, Values.PATH_A)
    Emitter.sub_sub_title("analysing C/CPP source files")
    Differ.diff_c_files(Definitions.FILE_DIFF_C)
    Emitter.sub_sub_title("analysing changed code segments")
    diff_info = Differ.diff_code(Definitions.FILE_DIFF_C, Definitions.FILE_TEMP_DIFF)


def analyse_ast_diff():
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    global diff_info
    diff_info = Differ.diff_ast(diff_info,
                                       Values.PATH_A,
                                       Values.PATH_B,
                                       Definitions.FILE_AST_SCRIPT)


def safe_exec(function_def, title, *args):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    start_time = time.time()
    Emitter.sub_title(title)
    description = title[0].lower() + title[1:]
    try:
        Logger.information("running " + str(function_def))
        if not args:
            result = function_def()
        else:
            result = function_def(*args)
        duration = str(time.time() - start_time)
        Emitter.success("\n\tSuccessful " + description + ", after " + duration + " seconds.")
    except Exception as exception:
        duration = str(time.time() - start_time)
        Emitter.error("Crash during " + description + ", after " + duration + " seconds.")
        error_exit(exception, "Unexpected error during " + description + ".")
    return result


def set_values():
    global FILE_DIFF_C, FILE_DIFF_H, FILE_DIFF_ALL
    global FILE_AST_SCRIPT, FILE_AST_DIFF_ERROR
    global FILE_EXCLUDED_EXTENSIONS, FILE_EXCLUDED_EXTENSIONS_A, FILE_EXCLUDED_EXTENSIONS_B


def analyse():
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    Emitter.title("Analysing changes")
    set_values()
    safe_exec(analyse_source_diff, "analysing source diff")
    safe_exec(analyse_ast_diff, "analysing ast diff")
