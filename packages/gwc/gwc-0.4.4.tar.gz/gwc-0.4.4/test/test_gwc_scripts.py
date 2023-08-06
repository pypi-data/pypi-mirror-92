import unittest
import mock
from gwc import gwc_scripts
import sys
from tempfile import TemporaryFile
import platform
import argparse

class TestGWCScripts(unittest.TestCase):

    @mock.patch("gdpy.api.Tasks.create_task")
    @mock.patch("gwc.gwc_scripts.read_configuration")
    @mock.patch("builtins.open" if platform.python_version_tuple()[0] == "3" else "__builtin__.open")
    @mock.patch("gwc.gwc_scripts.WorkflowApp._find_workflow")
    def test_run_workflow(self, mock_find_workflow, mock_open, mock_read_configuration, mock_create_task):
        mock_open.return_value = get_mock_file("{}")
        file_name = "input.json"
        mock_read_configuration.return_value = "endpoint", "access_id", "access_key", "account_name", "user_name"

        mock_find_workflow.return_value = {"workflow": "workflow", "version": "1"}, gwc_scripts.WDLWorkflow()
        testargs = ["", "workflow", "run", "-n", "many_layer_part_file", "-k", "true",
                    "-v", "1", "-a", "test", "-d", "run_dir", "-p", file_name]
        with mock.patch.object(sys, 'argv', testargs):
            gwc_scripts.main()
        self.assertEqual(mock_create_task.call_args[1]["parameters"]["keep_output_structure"], True)

        # test default --keep_output_structure
        testargs = ["", "workflow", "run", "-n", "many_layer_part_file",
                    "-v", "1", "-a", "test", "-d", "run_dir", "-p", file_name]

        mock_open.return_value = get_mock_file("{}")
        with mock.patch.object(sys, 'argv', testargs):
            gwc_scripts.main()
        self.assertEqual(mock_create_task.call_args[1]["parameters"]["keep_output_structure"], True)

        # test  --keep_output_structure false
        testargs = ["", "workflow", "run", "-n", "many_layer_part_file", "-k", "false",
                    "-v", "1", "-a", "test", "-d", "run_dir", "-p", file_name]

        mock_open.return_value = get_mock_file("{}")
        with mock.patch.object(sys, 'argv', testargs):
            gwc_scripts.main()
        self.assertEqual(mock_create_task.call_args[1]["parameters"]["keep_output_structure"], False)

    def test_str2bool(self):
        self.assertEqual(gwc_scripts.str2bool("yes"), True)
        self.assertEqual(gwc_scripts.str2bool("true"), True)
        self.assertEqual(gwc_scripts.str2bool("t"), True)
        self.assertEqual(gwc_scripts.str2bool("y"), True)
        self.assertEqual(gwc_scripts.str2bool("1"), True)
        self.assertEqual(gwc_scripts.str2bool("no"), False)
        self.assertEqual(gwc_scripts.str2bool("false"), False)
        self.assertEqual(gwc_scripts.str2bool("f"), False)
        self.assertEqual(gwc_scripts.str2bool("n"), False)
        self.assertEqual(gwc_scripts.str2bool("0"), False)
        with self.assertRaises(argparse.ArgumentTypeError):
            gwc_scripts.str2bool("error")
        with self.assertRaises(argparse.ArgumentTypeError):
            gwc_scripts.str2bool("==")


def get_mock_file(content):
    f = TemporaryFile(mode="w+")
    f.write(content)
    f.seek(0)
    return f


if __name__ == '__main__':
    unittest.main()
