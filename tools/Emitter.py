# -*- coding: utf-8 -*-

import sys
from common import Definitions, Values
from tools import Logger

GREY = '\t\x1b[1;30m'
RED = '\t\x1b[1;31m'
GREEN = '\x1b[1;32m'
YELLOW = '\t\x1b[1;33m'
BLUE = '\t\x1b[1;34m'
ROSE = '\t\x1b[1;35m'
CYAN = '\x1b[1;36m'
WHITE = '\t\x1b[1;37m'

PROG_OUTPUT_COLOR = '\t\x1b[0;30;47m'
STAT_COLOR = '\t\x1b[0;32;47m'


def write(print_message, print_color, new_line=True):
    if not Values.silence_emitter:
        r = "\033[K" + print_color + str(print_message) + '\x1b[0m'
        sys.stdout.write(r)
        if new_line:
            r = "\n"
            sys.stdout.write("\n")
        else:
            r = "\033[K\r"
            sys.stdout.write(r)
        sys.stdout.flush()


def title(title):
    write("\n" + "="*100 + "\n\n\t" + title + "\n" + "="*100+"\n", CYAN)
    Logger.information(title)


def sub_title(subtitle):
    write("\n\t" + subtitle + "\n\t" + "_"*90+"\n", CYAN)
    Logger.information(subtitle)


def sub_sub_title(sub_title):
    write("\n\t\t" + sub_title + "\n\t\t" + "-"*90+"\n", CYAN)
    Logger.information(sub_title)


def command(message):
    if Values.DEBUG:
        message = "running command\n\t" + message
        write(message, ROSE)
    Logger.command(message)


def normal(message, jump_line=True):
    write(message, BLUE, jump_line)
    # Logger.output(message)


def highlight(message, jump_line=True):
    write(message, WHITE, jump_line)


def information(message, jump_line=True):
    if Values.DEBUG:
        write(message, GREY, jump_line)
    Logger.information(message)


def statistics(message):
    write(message, GREY)
    Logger.output(message)


def error(message):
    write(message, RED)
    Logger.error(message)


def success(message):
    write(message, GREEN)
    Logger.output(message)


def special(message):
    write(message, ROSE)
    Logger.output(message)


def program_output(output_message):
    write("\t\tProgram Output:", WHITE)
    if type(output_message) == list:
        for line in output_message:
            write("\t\t\t" + line.strip(), PROG_OUTPUT_COLOR)
    else:
        write("\t\t\t" + output_message, PROG_OUTPUT_COLOR)


def emit_var_map(var_map):
    write("\t\tVar Map:", WHITE)
    for var_a in var_map:
        highlight("\t\t\t " + var_a + " ==> " + var_map[var_a])


def emit_ast_script(ast_script):
    write("\t\tAST Script:", WHITE)
    for line in ast_script:
        special("\t\t\t " + line.strip())


def warning(message):
    write(message, YELLOW)
    Logger.warning(message)


def debug(message):
    if Values.DEBUG:
        write(message, RED)
    Logger.warning(message)


def start():
    Logger.create()
    write("\n\n" + "#"*100 + "\n\n\tPatchWeave - Automated Patch Transplantation\n\n" + "#"*100, BLUE)


def end(time_info):
    Logger.end(time_info)
    statistics("\nRun time statistics:\n-----------------------\n")
    statistics("Initialization: " + time_info[Definitions.KEY_DURATION_INITIALIZATION] + " seconds")
    statistics("Build: " + time_info[Definitions.KEY_DURATION_EXPLOIT] + " seconds")
    statistics("Diff Analysis: " + time_info[Definitions.KEY_DURATION_DIFF_ANALYSIS] + " seconds")
    statistics("Trace Analysis: " + time_info[Definitions.KEY_DURATION_TRACE_ANALYSIS] + " seconds")
    statistics("Symbolic Trace Analysis: " + time_info[Definitions.KEY_DURATION_SYMBOLIC_TRACE_ANALYSIS] + " seconds")
    statistics("Slicing: " + time_info[Definitions.KEY_DURATION_SLICE] + " seconds")
    statistics("Transplantation: " + time_info[Definitions.KEY_DURATION_TRANSPLANTATION] + " seconds")
    statistics("Verification: " + time_info[Definitions.KEY_DURATION_VERIFICATION] + " seconds")
    success("\nPatchWeave finished successfully after " + time_info[Definitions.KEY_DURATION_TOTAL] + " seconds\n")


def help():
    print("Usage: python patchweave [OPTIONS] " + Definitions.ARG_CONF_FILE + "$FILE_PATH")
    print("Options are:")
    print("\t" + Definitions.ARG_DEBUG + "\t| " + "enable debugging information")
    print("\t" + Definitions.ARG_SKIP_TRACE_GEN + "\t| " + "disable project build")
    print("\t" + Definitions.ARG_SKIP_SYM_TRACE_GEN + "\t| " + "disable symbolic trace generation")
    print("\t" + Definitions.ARG_SKIP_VERIFY + "\t| " + "disable verification")
    print("\t" + Definitions.ARG_SKIP_WEAVE + "\t| " + "disable transplant")
    print("\t" + Definitions.ARG_SKIP_SLICE + "\t| " + "disable slicing")
    print("\t" + Definitions.ARG_SKIP_ANALYSE + "\t| " + "disable analysis")
