#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import time
from common.Utilities import error_exit
from common import Definitions, Values
from phases import Concolic, Analyse, Trace, Exploit
from tools import Logger, Solver, Fixer, Emitter, Weaver, Merger, Writer

function_list_a = list()
function_list_b = list()
function_list_c = list()
target_candidate_function_list = list()
mapping_ba = dict()
missing_function_list = dict()
missing_macro_list = dict()
missing_header_list = dict()
missing_data_type_list = dict()
modified_source_list = list()

var_expr_map_a = dict()
var_expr_map_b = dict()
var_expr_map_c = dict()

ast_map_a = dict()
ast_map_b = dict()
ast_map_c = dict()


FILE_VAR_EXPR_LOG_A = ""
FILE_VAR_EXPR_LOG_B = ""
FILE_VAR_EXPR_LOG_C = ""
FILE_VAR_VALUE_LOG_A = ""
FILE_VAR_VALUE_LOG_B = ""
FILE_VAR_VALUE_LOG_C = ""
FILE_VAR_MAP = ""
FILE_SKIP_LIST = ""
FILE_AST_SCRIPT = ""
FILE_TEMP_FIX = ""
FILE_FINAL_DIFF_OUTPUT = ""
FILE_LOCALIZATION_RESULT = ""


def get_sym_path_cond(source_location):
    sym_path_cond = ""
    if Values.PATH_A in source_location:
        # print(Concolic.sym_path_a.keys())
        for path in Trace.list_trace_a:
            # print(path)
            if path in Concolic.sym_path_a.keys():
                if Exploit.donor_crashed:
                    sym_path_cond = Concolic.sym_path_a[path][-1]
                else:
                    sym_path_cond = Concolic.sym_path_a[path][0]
            if path == source_location and sym_path_cond != "":
                # print(sym_path_cond)
                break
    elif Values.PATH_B in source_location:
        for path in Trace.list_trace_b:
            if path in Concolic.sym_path_b.keys():
                if Exploit.donor_crashed:
                    sym_path_cond = Concolic.sym_path_b[path][-1]
                else:
                    sym_path_cond = Concolic.sym_path_b[path][0]
            if path == source_location:
                break
    elif Values.PATH_C in source_location:
        for path in Trace.list_trace_c:
            if path in Concolic.sym_path_c.keys():
                if Exploit.target_crashed:
                    sym_path_cond = Concolic.sym_path_c[path][-1]
                else:
                    sym_path_cond = Concolic.sym_path_c[path][0]
            if path == source_location:
                break
    if sym_path_cond == "":
        Emitter.warning("\t\tWarning: no sym path found for " + source_location)
        return sym_path_cond
    return str(sym_path_cond)


def transplant_missing_header():
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    global modified_source_list, missing_header_list
    modified_source_list = Weaver.weave_headers(missing_header_list, modified_source_list)


def transplant_missing_macros():
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    global modified_source_list, missing_macro_list
    modified_source_list = Weaver.weave_definitions(missing_macro_list, modified_source_list)


def transplant_missing_data_types():
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    global modified_source_list, missing_data_type_list
    modified_source_list = Weaver.weave_data_type(missing_data_type_list, modified_source_list)


def transplant_missing_functions():
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    global missing_header_list, missing_macro_list, modified_source_list
    missing_header_list_func, \
    missing_macro_list_func, modified_source_list = Weaver.weave_functions(missing_function_list,
                                                                           modified_source_list,
                                                                           Concolic.sym_path_b)

    missing_macro_list = Merger.merge_macro_info(missing_macro_list, missing_macro_list_func)
    missing_header_list = Merger.merge_header_info(missing_header_list, missing_header_list_func)


def transplant_code():
    global missing_function_list, modified_source_list, missing_macro_list
    global missing_header_list, missing_data_type_list
    path_a = Values.PATH_A
    path_b = Values.PATH_B
    path_c = Values.PATH_C
    path_d = Values.Project_D.path
    sym_poc_path = Concolic.FILE_SYMBOLIC_POC
    poc_path = Values.PATH_POC
    bit_size = Concolic.VALUE_BIT_SIZE
    log_expr_info = FILE_VAR_EXPR_LOG_A, FILE_VAR_EXPR_LOG_B, FILE_VAR_EXPR_LOG_C
    log_value_info = FILE_VAR_VALUE_LOG_A, FILE_VAR_VALUE_LOG_B, FILE_VAR_VALUE_LOG_C
    log_file_info = log_expr_info, log_value_info
    out_file_info = FILE_SKIP_LIST, FILE_AST_SCRIPT, FILE_VAR_MAP
    file_info = out_file_info, log_file_info
    trace_list = Trace.list_trace_c
    stack_info_a = Trace.stack_a
    stack_info_c = Trace.stack_c
    suspicious_lines_c = Exploit.target_suspect_line_list
    # print(suspicious_lines_c)
    # print(Analyse.diff_info)
    for diff_loc in Values.diff_info.keys():
        Emitter.normal(diff_loc)
        diff_loc_info = Values.diff_info[diff_loc]
        div_sym_path_cond = get_sym_path_cond(diff_loc)
        last_sym_path_cond = Concolic.last_sym_path_c
        # print(last_sym_path_cond)
        estimate_loc, count_instant = Solver.estimate_divergent_point(div_sym_path_cond,
                                                       last_sym_path_cond,
                                                       Concolic.sym_path_c,
                                                       Trace.list_trace_c,
                                                       stack_info_c
                                                       )
        if not estimate_loc:
            Emitter.warning("\t\tWarning: no estimation for divergent point")
        else:
            estimate_loc = estimate_loc + ":" + str(count_instant)

        modified_source_list,\
        identified_missing_function_list,\
        identified_missing_macro_list,\
        identified_missing_header_list,\
        identified_missing_data_type_list = Weaver.weave_code(diff_loc,
                                                              diff_loc_info,
                                                              path_a,
                                                              path_b,
                                                              path_c,
                                                              path_d,
                                                              bit_size,
                                                              sym_poc_path,
                                                              poc_path,
                                                              file_info,
                                                              trace_list,
                                                              estimate_loc,
                                                              modified_source_list,
                                                              stack_info_a,
                                                              stack_info_c,
                                                              suspicious_lines_c)
        # print(identified_missing_function_list)
        if missing_function_list:
            if identified_missing_function_list:
                missing_function_list = missing_function_list.update(identified_missing_function_list)
        else:
            missing_function_list = identified_missing_function_list
        # print(missing_function_list)
        if missing_macro_list:
            if identified_missing_macro_list:
                missing_macro_list = Merger.merge_macro_info(missing_macro_list, identified_missing_macro_list)
        else:
            missing_macro_list = identified_missing_macro_list

        # print(identified_missing_header_list)
        if missing_header_list:
            if identified_missing_header_list:
                missing_header_list = Merger.merge_header_info(missing_header_list, identified_missing_header_list)
        else:
            missing_header_list = identified_missing_header_list

        # print(identified_missing_data_type_list)
        if missing_data_type_list:
            if identified_missing_data_type_list:
                missing_data_type_list = Merger.merge_data_type_info(missing_data_type_list, identified_missing_data_type_list)
        else:
            missing_data_type_list = identified_missing_data_type_list


def safe_exec(function_def, title, *args):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    start_time = time.time()
    Emitter.sub_title(title + "...")
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
    global FILE_VAR_EXPR_LOG_A, FILE_VAR_EXPR_LOG_B, FILE_VAR_EXPR_LOG_C
    global FILE_VAR_VALUE_LOG_A, FILE_VAR_VALUE_LOG_B, FILE_VAR_VALUE_LOG_C
    global FILE_VAR_MAP, FILE_SKIP_LIST, FILE_AST_SCRIPT
    global FILE_TEMP_FIX, FILE_MACRO_DEF, FILE_FINAL_DIFF_OUTPUT, FILE_LOCALIZATION_RESULT

    FILE_VAR_EXPR_LOG_A = Definitions.DIRECTORY_OUTPUT + "/log-sym-expr-a"
    FILE_VAR_EXPR_LOG_B = Definitions.DIRECTORY_OUTPUT + "/log-sym-expr-b"
    FILE_VAR_EXPR_LOG_C = Definitions.DIRECTORY_OUTPUT + "/log-sym-expr-c"
    FILE_VAR_VALUE_LOG_A = Definitions.DIRECTORY_OUTPUT + "/log-value-a"
    FILE_VAR_VALUE_LOG_B = Definitions.DIRECTORY_OUTPUT + "/log-value-b"
    FILE_VAR_VALUE_LOG_C = Definitions.DIRECTORY_OUTPUT + "/log-value-c"
    FILE_VAR_MAP = Definitions.DIRECTORY_OUTPUT + "/var-map"
    FILE_SKIP_LIST = Definitions.DIRECTORY_OUTPUT + "/skip-list"
    FILE_AST_SCRIPT = Definitions.DIRECTORY_OUTPUT + "/gen-ast-script"
    FILE_FINAL_DIFF_OUTPUT = Definitions.DIRECTORY_OUTPUT + "/patch-result"
    FILE_LOCALIZATION_RESULT = Definitions.DIRECTORY_OUTPUT + "/localization-result"


def save_values():
    global FILE_FINAL_DIFF_OUTPUT
    with open(FILE_FINAL_DIFF_OUTPUT, 'w') as diff_file:
        diff_file.writelines(Values.original_patch)
        diff_file.writelines(["\n\n=============================================\n\n"])
        diff_file.writelines(Values.transplanted_patch)
    with open(FILE_LOCALIZATION_RESULT, 'w') as result_file:
        result_file.writelines(["Localized Count:" + str(len(Values.localized_function_list))])
        result_file.writelines(["Non-Localized Count:" + str(len(Values.non_localized_function_list))])
        result_file.writelines(["Find Count:" + str(Values.localization_iteration_no)])


def weave():
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    Emitter.title("Repairing vulnerability")
    set_values()
    if not Values.SKIP_WEAVE:
        safe_exec(transplant_code, "transplanting code")
        safe_exec(transplant_missing_functions, "transplanting functions")
        safe_exec(transplant_missing_data_types, "transplanting data structures")
        safe_exec(transplant_missing_macros, "transplanting macros")
        safe_exec(transplant_missing_header, "transplanting header files")
        safe_exec(Fixer.check, "correcting syntax errors", modified_source_list)
    save_values()
