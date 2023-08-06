import os
import unittest

from module_for_cli_test import __main__ as example_main
from module_for_cli_test.__main__ import ascii_logo
from simppl.cli import CommandLineInterface


class TestCliExplicitMode(unittest.TestCase):

    def test_cli_no_params(self):
        cli = CommandLineInterface(example_main.__file__, ascii_logo, [])
        cli.run(['my_tool_box'])

    def test_cli_add_two_numbers_example(self):
        import module_for_cli_test.add_two_numbers
        modules_list = [module_for_cli_test.add_two_numbers]
        cli = CommandLineInterface(example_main.__file__, ascii_logo, modules_list)
        return_value = cli.run(['my_tool_box', 'add_two_numbers', '1.5', '2'])
        self.assertEqual(0, return_value)

    def test_cli_analyze_file_pipeline_example(self):
        
        cli = CommandLineInterface(example_main.__file__, ascii_logo)
        project_dir = os.path.dirname(os.path.dirname(__file__))
        return_value = cli.run(['my_tool_box', 'analyze_file_pipeline',
                                f'{project_dir}/tests/resources/analyze_file_pipeline_input.txt',
                                'test_outputs'])
        self.assertEqual(0, return_value)
