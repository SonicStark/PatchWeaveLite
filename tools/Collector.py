#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import os
import Emitter
import Logger


def collect_symbolic_expressions(trace_file_path):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    Emitter.normal("\t\tcollecting symbolic expressions")
    var_expr_map = dict()
    if os.path.exists(trace_file_path):
        with open(trace_file_path, 'r') as trace_file:
            for line in trace_file:
                if '[var-expr]' in line:
                    line = line.replace("[var-expr] ", "")
                    var_name, var_expr = line.split(":")
                    var_expr_map[var_name] = var_expr.replace("\n", "")
    return var_expr_map


def collect_symbolic_path(file_path, project_path):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    Emitter.normal("\tcollecting symbolic path conditions")
    constraints = dict()
    if os.path.exists(file_path):
        source_path = ""
        path_condition = ""
        with open(file_path, 'r') as trace_file:
            for line in trace_file:
                if '[path:condition]' in line:
                    if project_path in line:
                        source_path = str(line.replace("[path:condition]", '')).split(" : ")[0]
                        source_path = source_path.strip()
                        source_path = os.path.abspath(source_path)
                        path_condition = str(line.replace("[path:condition]", '')).split(" : ")[1]
                        continue
                if source_path:
                    if "(exit)" not in line:
                        path_condition = path_condition + line
                    else:
                        constraints[source_path] = path_condition
                        source_path = ""
                        path_condition = ""
    return constraints


def collect_trace(file_path, project_path, suspicious_loc_list):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    Emitter.normal("\tcollecting trace")
    list_trace = list()
    if os.path.exists(file_path):
        with open(file_path, 'r') as trace_file:
            for line in trace_file:
                if '[trace]' in line:
                    if project_path in line:
                        trace_line = str(line.replace("[trace]", '')).split(" - ")[0]
                        trace_line = trace_line.strip()
                        if (not list_trace) or (list_trace[-1] != trace_line):
                            list_trace.append(trace_line)
                        if any(loc in line for loc in suspicious_loc_list):
                            break
    return list_trace


def collect_suspicious_points(trace_log):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    Emitter.normal("\textracting crash point")
    suspect_list = list()
    if os.path.exists(trace_log):
        with open(trace_log, 'r') as trace_file:
            for read_line in trace_file:
                if "runtime error:" in read_line:
                    crash_location = read_line.split(": runtime error: ")[0]
                    crash_location = ":".join(crash_location.split(":")[:-1])
                    if crash_location not in suspect_list:
                        suspect_list.append(crash_location)
    return suspect_list


def collect_crash_point(trace_file_path):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    Emitter.normal("\textracting crash point")
    crash_location = ""
    if os.path.exists(trace_file_path):
        with open(trace_file_path, 'r') as trace_file:
            for read_line in trace_file:
                if "KLEE: ERROR:" in read_line:
                    read_line = read_line.replace("KLEE: ERROR: ", "")
                    crash_location = read_line.split(": ")[0]
                    break
    return crash_location


def collect_stack_info(trace_file_path):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    Emitter.normal("\textracting stack information")
    stack_map = dict()
    if os.path.exists(trace_file_path):
        with open(trace_file_path, 'r') as trace_file:
            is_stack = False
            for read_line in trace_file:
                if is_stack and '#' in read_line:
                    if " at " in read_line:
                        read_line, source_path = str(read_line).split(" at ")
                        source_path, line_number = source_path.split(":")
                        function_name = str(read_line.split(" in ")[1]).split(" (")[0]
                        if source_path not in stack_map.keys():
                            stack_map[source_path] = dict()
                        stack_map[source_path][function_name] = line_number
                if "Stack:" in read_line:
                    is_stack = True
                    continue
    return stack_map
