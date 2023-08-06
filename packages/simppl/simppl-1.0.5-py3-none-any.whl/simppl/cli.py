import importlib
import os
import re
import argparse
import sys
from argparse import ArgumentParser
from collections import defaultdict
from functools import wraps
from typing import List

from colorama import Fore
from simppl.simple_pipeline import SimplePipeline


class CommandLineInterface:

    def __init__(self, main_path: str, module_ascii_logo: str, modules_list: list = None):
        self.cli_ascii_logo = module_ascii_logo
        self.cli_path = os.path.dirname(main_path)
        self.cli_name = os.path.basename(self.cli_path)
        self.modules_list: list = modules_list
        self.command_line_tools = defaultdict(dict)
        self.tool_name_to_package = defaultdict()
        if modules_list is None:
            self.__load_tools()
        else:
            self.__add_tools_from_list()

    def print_usage(self):
        print(Fore.GREEN + self.cli_ascii_logo)
        print(Fore.RED + f'\tUsage: python -m {self.cli_name} <tool_name> <arg1, arg2, ...>\n')
        print(Fore.RESET + 'Tools list:')
        print('-----------\n')
        for package_name in sorted(self.command_line_tools):
            print(Fore.LIGHTMAGENTA_EX + f'package {package_name}:')
            for tool_name in sorted(self.command_line_tools[package_name]):
                print(Fore.CYAN + f'\t{tool_name}:')
                description = self.command_line_tools[package_name][tool_name].__doc__
                description = description.strip()
                lines = description.split('\n')
                for line in lines:
                    print(Fore.RESET + f'\t\t{line.strip()}')
                print('')
        return ''

    # Add new tools to and return as map<package, tool_name, command_line_tool_run_method>
    def __load_tools(self):
        script_dir = self.cli_path
        root_dir = os.path.dirname(self.cli_path) + os.sep

        for subdir, dirs, files in os.walk(script_dir):
            # skip non python package dirs
            if '__init__.py' not in files:
                continue

            for file in files:
                file_path = subdir + os.sep + file

                if file_path.endswith(".py"):
                    found_tool_definition = False
                    module_str = file_path.replace(root_dir, '').replace(os.sep, '.')
                    module_str = re.sub('.py$', '', module_str)
                    with open(file_path, encoding='utf8') as fh:
                        for line in fh:
                            line = line.strip()
                            if line == '@command_line_tool':
                                found_tool_definition = True
                            if found_tool_definition:
                                module = importlib.import_module(module_str)
                                package_name = module_str.split('.')[-2]
                                module_name = module_str.split('.')[-1]
                                if package_name not in self.command_line_tools:
                                    self.command_line_tools[package_name] = {}
                                try:
                                    if module.run.__doc__ is None:
                                        raise RuntimeError(f'Must define a docstring for command_line_tool: {module_str}')
                                except AttributeError:
                                    raise RuntimeError(
                                        f'command_line_tool module {module_str} must implement a run method.')

                                self.command_line_tools[package_name][module_name] = module.run
                                self.tool_name_to_package[module_name] = package_name

    def run(self, argv):
        if len(argv) == 1:
            self.print_usage()
            return 0

        tool_name = argv[1]
        package = self.command_line_tools[self.tool_name_to_package[tool_name]]

        if tool_name in package:
            exit_code = self.__run_tool(tool_name, package, argv[1:])
            return exit_code
        else:
            raise RuntimeError(f'Could not find tool: {tool_name} \n{self.print_usage()}')

    def __add_tools_from_list(self):
        for tool in self.modules_list:
            tool_name = tool.__name__.split('.')[-1]
            package = tool.__package__
            self.command_line_tools[package][tool_name] = tool.run
            self.tool_name_to_package[tool_name] = package

    @staticmethod
    def __run_tool(tool_name: str, package: dict, argv: List[str]) -> int:
        exit_code = package[tool_name](argv)
        # interpret run method with no return value as successful run
        if exit_code is None:
            exit_code = 0
        return exit_code


def print_args(argv):
    sys.stderr.write('python -m <module_name>')
    key = None
    for field in argv:
        if field.startswith('-'):
            if key is None:
                key = field
            else:
                sys.stderr.write(f' {key}')
                key = field
        else:
            if key is None:
                sys.stderr.write(f' {field} ')
            else:
                sys.stderr.write(f' {key} {field}')
                key = None
    sys.stderr.write('\n')


def command_line_tool(run_function):
    @wraps(run_function)
    def wrapper(argv):
        # print command if not internal_tool (which was ran from another tool)
        if argv[0] != 'internal_tool':
            print_args(argv)

        if run_function.__doc__ is None:
            raise RuntimeError(f'Must define a docstring for command_line_tool: {run_function.__module__}')
        if run_function.__name__ != 'run':
            raise RuntimeError(f'only functions named "run" can be a command_line_tool, got: {run_function.__name__}')
        run_function(argv)

    return wrapper


def get_simple_pipeline(arg_parser: ArgumentParser, argv: list, name):
    """
    :param arg_parser: argument parser, will add SimplePipeline arguments to it
    :param argv: arguments list of command_line_tool
    :param name: __name__ of calling module, used in logging
    :return: simple_pipeline object
    """
    SimplePipeline.add_parse_args(arg_parser)
    args = arg_parser.parse_args(argv[1:])
    return SimplePipeline(args.fc, args.lc, debug=args.d, print_timing=True, name=name)


def get_parser(prog, description):
    """
    :param prog: command_line_tool name (argv[0])
    :param description: command_line_tool description (__doc__)
    :return: argument parser
    """
    return argparse.ArgumentParser(description=description, prog=prog,
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
