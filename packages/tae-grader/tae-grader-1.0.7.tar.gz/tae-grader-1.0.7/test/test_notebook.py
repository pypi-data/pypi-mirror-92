##################################
##### Tests for taeg notebook #####
##################################

import unittest
import sys
import os
import shutil
import subprocess
import json
import requests
import nbformat

from glob import glob
from subprocess import PIPE
from unittest.mock import patch
from unittest import mock

from taeg import Notebook
from taeg.check.logs import LogEntry, EventType, Log
from taeg.check.notebook import _TAEG_LOG_FILENAME
from taeg.check import notebook
# from taeg import TestsDisplay

from . import TestCase

TEST_FILES_PATH = "test/test-notebook/"


# functions used in one of the tests below
def square(x):
    return x ** 2

def negate(x):
    return not x

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.text = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == "http://some.url/auth/google":
        return MockResponse({"text": "value1"}, 200)
    elif args[0] == "http://some.url/submit":
        return MockResponse({"text": "this is the fake submit post response"}, 200)
    elif args[0] == "http://some.url/track":
        return MockResponse({"text": "this is the fake track post response"}, 200)

    return MockResponse(None, 404)

def mock_auth_get():
    class AuthResponse:
        def __init__(self, json_data, status_code):
            self.content = json_data
            self.status_code = status_code

        def content(self):
            return self

        def decode(self, type):
            return "fakekey"

    str = "fakekey"
    content = str.encode("utf-8", "strict")
    response = AuthResponse(content, 2)

    return response


class TestNotebook(TestCase):
    """
    Test cases for the ``Notebook`` class
    """


    # Checks that the taeg.Notebook class init works correctly
    def test_init_1(self):

        """
        taeg_configs exists, _service_enabled = True, auth exists
        """
        notebook._API_KEY = 'fakekey'

        # Set up taeg_config file
        variables = {
            "arr": "numpy.ndarray"
        }

        config = {
            "notebook": TEST_FILES_PATH + "hw00.ipynb",
            "endpoint": "http://some.url", # dont include this when testing service enabled stuff
            "assignment_id": "hw00",
            "class_id": "some_class",
            "auth": "google",
            "save_environment": False,
            "ignore_modules": [],
            "variables": variables
        }

        # Make new taeg config file, put it in direcotry
        f = open("demofile2.taeg", "w+")
        f.write(json.dumps(config))
        f.close()

        # Instance of Notebook class
        grader = Notebook(TEST_FILES_PATH + "tests")

        for q_path in glob(TEST_FILES_PATH + "tests/*.py"):
            q = os.path.split(q_path)[1][:-3]

            # Checks to make sure Notebook took in the config file correctly
            self.assertEqual(grader._ignore_modules, config['ignore_modules'], "Test {} init (ignore modules) failed".format(q))
            self.assertEqual(grader._service_enabled, True, "Test {} init (service enabled) failed".format(q))
            self.assertEqual(grader._vars_to_store, config['variables'], "Test {} init (variables) failed".format(q))
            self.assertEqual(grader._notebook, config['notebook'], "Test {} init (notebook) failed".format(q))
            self.assertEqual(grader._config['auth'], config['auth'], "Test {} init (auth) failed".format(q))

            self.assertEqual(grader._google_auth_url, "http://some.url/auth/google", "Test {} init (google auth url) failed".format(q))
            self.assertEqual(grader._default_auth_url, "http://some.url/auth", "Test {} init (default auth url) failed".format(q))
            self.assertEqual(grader._submit_url, "http://some.url/submit", "Test {} init (submit url) failed".format(q))





    def test_init_2(self):
        """
        taeg_configs exists, _service_enabled = True, auth does not exist
        """

        notebook._API_KEY = 'fakekey'


        variables = {
            "arr": "numpy.ndarray"
        }

        config2 = {
            "notebook": TEST_FILES_PATH + "hw00.ipynb",
            "endpoint": "http://some.url", # dont include this when testing service enabled stuff
            "assignment_id": "hw00",
            "class_id": "some_class",
            "save_environment": False,
            "ignore_modules": [],
            "variables": variables
        }

        # Make new taeg config file, put it in direcotry
        f = open("demofile3.taeg", "a")
        f.write(json.dumps(config2))
        f.close()

        # Instance of Notebook class
        grader = Notebook(TEST_FILES_PATH + "tests")


        for q_path in glob(TEST_FILES_PATH + "tests/*.py"):
            q = os.path.split(q_path)[1][:-3]
            self.assertEqual(grader._ignore_modules, config2['ignore_modules'], "Test {} init (ignore modules) failed".format(q))
            self.assertEqual(grader._service_enabled, True, "Test {} init (service enabled) failed".format(q))
            self.assertEqual(grader._vars_to_store, config2['variables'], "Test {} init (variables) failed".format(q))
            self.assertEqual(grader._notebook, config2['notebook'], "Test {} init (notebook) failed".format(q))
            self.assertEqual(grader._config['auth'], 'google', "Test {} init (auth) failed".format(q))
            self.assertEqual(grader._google_auth_url, "http://some.url/auth/google", "Test {} init (google auth url) failed".format(q))
            self.assertEqual(grader._default_auth_url, "http://some.url/auth", "Test {} init (default auth url) failed".format(q))
            self.assertEqual(grader._submit_url, "http://some.url/submit", "Test {} init (submit url) failed".format(q))

    def test_init_3(self):
        """
        More than 1 taeg_config
        """

        variables = {
            "arr": "numpy.ndarray"
        }

        config2 = {
            "notebook": TEST_FILES_PATH + "hw00.ipynb",
            "endpoint": "http://some.url", # dont include this when testing service enabled stuff
            "assignment_id": "hw00",
            "class_id": "some_class",
            "save_environment": False,
            "ignore_modules": [],
            "variables": variables
        }

        f = open("demofile4.taeg", "a")
        f.write(json.dumps(config2))
        f.close()

        f2 = open("demofile5.taeg", "a")
        f2.write(json.dumps(config2))
        f2.close()

        # Instance of Notebook class, should throw Exception
        with self.assertRaises(Exception):
            Notebook(TEST_FILES_PATH + "tests")


    # These tests check to see that auth correctly authorizes a student, based off
    # the student-inputted config file
    @mock.patch('builtins.input', return_value='fakekey')
    def test_auth_1(self, mock_get):
        """
        taeg_configs exists, _service_enabled = True, auth exists but incorrect
        and should throw an exception (case where auth does not exist covered in init)
        """
        notebook._API_KEY = None

        variables = {
            "arr": "numpy.ndarray"
        }

        config = {
            "notebook": TEST_FILES_PATH + "hw00.ipynb",
            "endpoint": "http://some.url", # dont include this when testing service enabled stuff
            "assignment_id": "hw00",
            "class_id": "some_class",
            "auth": "googe",
            "save_environment": False,
            "ignore_modules": [],
            "variables": variables
        }

        # Make new taeg config file, put it in direcotry
        f = open("demofile6.taeg", "a")
        f.write(json.dumps(config))
        f.close()

        # Instance of Notebook class
        with self.assertRaises(Exception):
            Notebook(TEST_FILES_PATH + "tests")


    @mock.patch('builtins.input')
    def test_auth_2(self, mock_input):
        """
        taeg_configs exists, _service_enabled = True, auth is google
        and not should throw an exception (goes into google if statement)
        """
        notebook._API_KEY = None
        # set up mock input
        mock_input.return_value = "fakekey"

        variables = {
            "arr": "numpy.ndarray"
        }

        config = {
            "notebook": TEST_FILES_PATH + "hw00.ipynb",
            "endpoint": "http://some.url", # dont include this when testing service enabled stuff
            "assignment_id": "hw00",
            "class_id": "some_class",
            "auth": "google",
            "save_environment": False,
            "ignore_modules": [],
            "variables": variables
            }

        # Make new taeg config file, put it in direcotry
        f = open("demofile6.taeg", "a")
        f.write(json.dumps(config))
        f.close()

        # Instance of Notebook class
        grader = Notebook(TEST_FILES_PATH + "tests")

        self.assertEqual(grader._api_key, "fakekey")


    @mock.patch('builtins.input')
    def test_auth_3(self, mock_input):
        """
        taeg_configs exists, _service_enabled = True, auth is automatically set
        and not should throw an exception, _API_KEY exists from test_auth_2
        """
        # set up mock input
        mock_input.return_value='fake input'


        variables = {
            "arr": "numpy.ndarray"
        }

        config = {
            "notebook": TEST_FILES_PATH + "hw00.ipynb",
            "endpoint": "http://some.url", # dont include this when testing service enabled stuff
            "assignment_id": "hw00",
            "class_id": "some_class",
            "auth": "default",
            "save_environment": False,
            "ignore_modules": [],
            "variables": variables
            }

        # Make new taeg config file, put it in direcotry
        f = open("demofile6.taeg", "a")
        f.write(json.dumps(config))
        f.close()

        # Instance of Notebook class
        grader = Notebook(TEST_FILES_PATH + "tests")

        self.assertEqual(grader._api_key, "fakekey")

    @mock.patch('taeg.check.notebook.requests.get')
    @mock.patch('taeg.check.notebook.getpass')
    @mock.patch('taeg.check.notebook.input')
    def test_auth_4(self, mock_input, mock_pass, mock_get):
        """
        taeg_configs exists, _service_enabled = True, auth is automatically set
        and not should throw an exception, _API_KEY exists from test_auth_2
        """
        # sets api_key to none to avoid first if statement in notebook.auth()
        notebook._API_KEY = None

        # sets up methods to mock
        mock_get.return_value = mock_auth_get()
        mock_pass.return_value = "fake pass"
        mock_input.return_value = "fake input"

        variables = {
            "arr": "numpy.ndarray"
        }


        config = {
            "notebook": TEST_FILES_PATH + "hw00.ipynb",
            "endpoint": "http://some.url",
            "assignment_id": "hw00",
            "class_id": "some_class",
            "auth": "default",
            "save_environment": False,
            "ignore_modules": [],
            "variables": variables
            }

        # Make new taeg config file, put it in direcotry
        f = open("demofile6.taeg", "a")
        f.write(json.dumps(config))
        f.close()

        # Instance of Notebook class
        grader = Notebook(TEST_FILES_PATH + "tests")

        self.assertEqual(grader._api_key, "fakekey")

    # These tests check to see that notebook.submit() correctly posts an assignment
    def test_submit_1(self):
        """
        _service_enabled = False, should raise an exception
        """
        variables = {
            "arr": "numpy.ndarray"
        }

        # Instance of Notebook class
        with self.assertRaises(Exception):
            grader = Notebook(TEST_FILES_PATH + "tests")
            grader.submit()

    @mock.patch('taeg.check.notebook.requests.post', side_effect=mocked_requests_get)
    def test_submit_2(self, mock_get):
        """
        taeg_configs exists, _service_enabled = True, should go not into auth
        and run as it should
        """
        variables = {
            "arr": "numpy.ndarray"
        }

        config = {
            "notebook": TEST_FILES_PATH + "hw00.ipynb",
            "assignment_id": "hw00",
            "class_id": "some_class",
            "auth": "google",
            "save_environment": False,
            "ignore_modules": [],
            "variables": variables,
            "endpoint": "http://some.url",
                    }

        f = open("demofile6.taeg", "a")
        f.write(json.dumps(config))
        f.close()

        grader = Notebook(TEST_FILES_PATH + "tests")
        grader.submit()

        #check to see if the right file was used
        args, kwargs = mock_get.call_args
        self.assertEqual(config['endpoint'] + '/submit', args[0])

    def test_submit_3(self):
        notebook._API_KEY = "fakekey for submit"
        config = {
            "notebook": TEST_FILES_PATH + "hw00.ipynb",
            "assignment_id": "hw00",
            "class_id": "some_class",
            "save_environment": False,
            "ignore_modules": [],
            "variables": variables,
            "endpoint": "http://some.url",
                    }
        """
        taeg_configs exists, _service_enabled = True, should go into auth if statement
        """

    @mock.patch('taeg.check.notebook.hasattr')
    @mock.patch('taeg.check.notebook.requests.post', side_effect=mocked_requests_get)
    def test_submit_3(self, mock_get, mock_hasattr):
        # mock_get.side_effect=mocked_requests_get
        mock_hasattr.return_value = None



        """
        taeg_configs exists, _service_enabled = True, should go not into auth
        and run as it should
        """
        variables = {
            "arr": "numpy.ndarray"
        }

        config = {
            "notebook": TEST_FILES_PATH + "hw00.ipynb",
            "assignment_id": "hw00",
            "class_id": "some_class",
            "save_environment": False,
            "ignore_modules": [],
            "variables": variables,
            "endpoint": "http://some.url",
                    }

        f = open("demofile6.taeg", "a")
        f.write(json.dumps(config))
        f.close()

        grader = Notebook(TEST_FILES_PATH + "tests")
        grader.submit()

        #check to see if the right file was used
        args, kwargs = mock_get.call_args
        self.assertEqual(config['endpoint'] + '/submit', args[0])


    @mock.patch('taeg.check.notebook.requests.post', side_effect=mocked_requests_get)
    def test_track(self, mock_post):
        """
        Checks that the taeg.Notebook class works correctly
        """
        notebook._API_KEY = 'fakekey'

        config = {
            "notebook": TEST_FILES_PATH + "hw00.ipynb",
            "assignment_url": "http://assignment.url",
            "assignment_id": "hw00",
            "class_id": "some_class",
            "save_environment": False,
            "ignore_modules": [],
            "variables": {},
            "endpoint": "http://some.url",
        }
        f = open("demofile6.taeg", "a")
        f.write(json.dumps(config))
        f.close()

        # i1 = Notebook(TEST_FILES_PATH + "tests") #bypass setup
        grader = Notebook(TEST_FILES_PATH + "tests")

        def square(x):
            return x ** 2

        def negate(x):
            return not x

        global_env = {
            "square": square,
            "negate": negate
        }

        result = grader.check('q1', global_env=global_env)
        # for q_path in glob(TEST_FILES_PATH + "tests/*.py"):
        #     q = os.path.split(q_path)[1][:-3]
        #     if q != "q2":
        #         self.assertEqual(result.grade, 1, "Test {} failed".format(q))
        #     else:
        #         self.assertEqual(result.grade, 0, "Test {} passed".format(q))

        #check to see if the right file was used
        args, kwargs = mock_post.call_args
        self.assertEqual(config['endpoint'] + '/track', args[0])
        self.assertTrue('grade' in args[1])
        self.assertTrue('class_id' in args[1])
        self.assertTrue('assignment_id' in args[1])
        self.assertTrue('question_id' in args[1])


    def test_repr(self):

        #class to mock TestCollectionResults
        class FakeTestCollectionResult:

            def _repr_html_(self):
                return "Fake test collection result"

        #result variable
        test = [("t1", FakeTestCollectionResult()), ("t2", FakeTestCollectionResult())]
        
        try:
            a = notebook.TestsDisplay(test)
            a._repr_html_()
        except Exception:
            self.fail("test_repr failed")



    @mock.patch('builtins.input', return_value='fakekey')
    def test_check_local(self, mock_input):
        """
        Checks that the taeg.Notebook class works correctly
        """
        notebook._API_KEY = 'fakekey'

        # i1 = Notebook(TEST_FILES_PATH + "tests") #bypass setup
        grader = Notebook(TEST_FILES_PATH + "tests")

        def square(x):
            return x ** 2

        def negate(x):
            return not x

        global_env = {
            "square": square,
            "negate": negate
        }

        for q_path in glob(TEST_FILES_PATH + "tests/*.py"):
            q = os.path.split(q_path)[1][:-3]
            result = grader.check_local(q, global_env=global_env)
            if q != "q2":
                self.assertEqual(result.grade, 1, "Test {} failed".format(q))
            else:
                self.assertEqual(result.grade, 0, "Test {} passed".format(q))

    def test_check_no_env(self):
        """
        Checks that the ``Notebook`` class works correctly, with no global env input
        """
        grader = Notebook(TEST_FILES_PATH + "tests")

        for q_path in glob(TEST_FILES_PATH + "tests/*.py"):
            q = os.path.split(q_path)[1][:-3]
            result = grader.check_local(q)  # global_env=global_env)
            if q != "q2":
                self.assertEqual(result.grade, 1, f"Test {q} expected to pass but failed:\n{result}")
            else:
                self.assertEqual(result.grade, 0, f"Test {q} expected to fail but passed:\n{result}")

    def test_check_raise_exception(self):
        """
        Checks that the taeg.Notebook class check method correctly raises Exceptions
        when things go wrong
        """
        grader = Notebook(TEST_FILES_PATH + "tests")
        global_env = 0
        for q_path in glob(TEST_FILES_PATH + "tests/*.py"):
            q = os.path.split(q_path)[1][:-3]
            self.assertRaises(AttributeError,
                              lambda: grader.check_local(q, global_env=global_env))

    def test_check_all_repr(self):
        """
        Checks that the representation of results as strings is correct
        """
        grader = Notebook(TEST_FILES_PATH + "tests")

        output = str(grader.check_all())

        # checks each question substring
        output_lst = [
            'q1:\n\n    All tests passed!\n',
            'q2:\n\n    \n    0 of 1 tests passed\n',
            'q3:\n\n    All tests passed!\n',
            'q4:\n\n    All tests passed!\n',
            'q5:\n\n    All tests passed!\n'
        ]

        for result in output_lst:
            self.assertTrue(output.count(result) == 1)

    def test_to_pdf_with_nb_path(self):
        """
        Checks for existence of notebook PDF
        This test is the general use case WITH a specified notebook path
        """
        nb = nbformat.v4.new_notebook()
        text = """\
        This is an auto-generated notebook."""
        nb['cells'] = [nbformat.v4.new_markdown_cell(text)]
        with open(TEST_FILES_PATH + 'test-nb.ipynb', "w") as f:
            nbformat.write(nb, f)
        grader = Notebook(TEST_FILES_PATH + "tests")
        grader.to_pdf(TEST_FILES_PATH + "test-nb.ipynb", filtering=False)

        self.assertTrue(os.path.isfile(TEST_FILES_PATH + "test-nb.pdf"))
        # cleanup
        os.remove(TEST_FILES_PATH + 'test-nb.ipynb')
        os.remove(TEST_FILES_PATH + "test-nb.pdf")

    @mock.patch('builtins.input', return_value='fakekey')
    def test_to_pdf_without_nb_path_case1_pass(self, mockInp):
        """
        Checks for the existence of notebook PDF
        This test is for the case where notebook path is not defined,
        but there exists a .taeg file specifying the IPYNB notebook name
        """
        config = {
            "notebook": TEST_FILES_PATH + "test-nb.ipynb",
            "endpoint": "http://some.url",  # dont include this when testing service enabled stuff
            "assignment_id": "hw00",
            "class_id": "some_class",
            "auth": "google",
            "save_environment": False,
            "ignore_modules": [],
        }
        # Make new taeg file, put it in directory
        f = open("demofile2.taeg", "w")
        f.write(json.dumps(config))
        f.close()
        nb = nbformat.v4.new_notebook()
        text = """\
                This is an auto-generated notebook."""
        nb['cells'] = [nbformat.v4.new_markdown_cell(text)]
        with open(TEST_FILES_PATH + 'test-nb.ipynb', "w") as f:
            nbformat.write(nb, f)
        grader = Notebook(TEST_FILES_PATH + "tests")
        grader.to_pdf(nb_path = None, filtering=False)
        self.assertTrue(os.path.exists(TEST_FILES_PATH + "test-nb.pdf"))
        # cleanup
        os.remove(TEST_FILES_PATH + 'test-nb.ipynb')
        os.remove(TEST_FILES_PATH + "test-nb.pdf")
        os.remove("demofile2.taeg")

    def test_to_pdf_without_nb_path_case2_fail(self):
        """
        Checks for correct error scenario for to_pdf method
        This test is for when np_path is set to None and multiple
        IPYNB notebooks exist in the working directory.
        """
        nb1 = nbformat.v4.new_notebook()
        nb2 = nbformat.v4.new_notebook()
        text = """\
                This is an auto-generated notebook."""
        nb1['cells'] = [nbformat.v4.new_markdown_cell(text)]
        nb2['cells'] = [nbformat.v4.new_markdown_cell(text)]
        with open('test-nb1.ipynb', "w") as f:
            nbformat.write(nb1, f)
        with open('test-nb2.ipynb', "w") as f:
            nbformat.write(nb2, f)
        grader = Notebook(TEST_FILES_PATH + "tests")
        self.assertRaises(AssertionError,
                          lambda: grader.to_pdf(nb_path=None, filtering=False))
        os.remove('test-nb1.ipynb')
        os.remove('test-nb2.ipynb')

    def test_export_pass(self):
        """
        Checks export contents for existence of PDF and equality of zip
        """
        nb = nbformat.v4.new_notebook()
        text = """\
                        This is an auto-generated notebook."""
        nb['cells'] = [nbformat.v4.new_markdown_cell(text)]
        with open(TEST_FILES_PATH + 'test-nb.ipynb', "w") as f:
            nbformat.write(nb, f)
        correct_directory = TEST_FILES_PATH + 'export-correct/'
        os.mkdir(correct_directory)
        with open(correct_directory + 'test-nb.ipynb', "w") as f:
            nbformat.write(nb, f)
        grader = Notebook(TEST_FILES_PATH + "tests")
        grader.export(TEST_FILES_PATH + "test-nb.ipynb", filtering=False)

        self.assertTrue(os.path.isfile(TEST_FILES_PATH + "test-nb.pdf"))
        with self.unzip_to_temp(TEST_FILES_PATH + "test-nb.zip") as unzipped_dir:
            # breakpoint()
            os.remove(unzipped_dir + '/test/test-notebook/test-nb.pdf')
            self.assertDirsEqual(
                unzipped_dir + '/test/test-notebook/',
                TEST_FILES_PATH + "export-correct",
                ignore_ext=[".pdf"]
            )

        # cleanup
        os.remove(correct_directory + "test-nb.ipynb")
        os.rmdir(correct_directory)
        os.remove(TEST_FILES_PATH + "test-nb.ipynb")
        os.remove(TEST_FILES_PATH + "test-nb.pdf")
        os.remove(TEST_FILES_PATH + "test-nb.zip")

    def test_export_without_nb_path_case2_fail(self):
        """
        Checks for correct error scenario for export method
        This test is for when nb_path is set to None and
        there are multiple IPYNB notebooks in working directory
        """
        nb1 = nbformat.v4.new_notebook()
        nb2 = nbformat.v4.new_notebook()
        text = """\
                        This is an auto-generated notebook."""
        nb1['cells'] = [nbformat.v4.new_markdown_cell(text)]
        nb2['cells'] = [nbformat.v4.new_markdown_cell(text)]
        with open('test-nb1.ipynb', "w") as f:
            nbformat.write(nb1, f)
        with open('test-nb2.ipynb', "w") as f:
            nbformat.write(nb2, f)
        grader = Notebook(TEST_FILES_PATH + "tests")
        self.assertRaises(AssertionError,
                          lambda: grader.export(nb_path=None, filtering=False))
        os.remove('test-nb1.ipynb')
        os.remove('test-nb2.ipynb')

    def test_export_without_nb_path_case3(self):
        """
        Checks for correct error scenario for export method
        This test is for when nb_path is set to None and
        there are no IPYNB notebooks in the working directory
        """
        files_in_directory = os.listdir('./')
        notebooks = [file for file in files_in_directory if file.endswith(".ipynb")]
        for file in notebooks:
            os.remove('./' + file)
        grader = Notebook()
        self.assertRaises(ValueError,
                          lambda: grader.export(nb_path=None, filtering=False))

    def test_export_multiple_taeg_error(self):
        """
        Checks export for error scenario for export method
        This test should pass when export successfully raises an
        AssertionError for the case when the directory contains
        multiple .taeg files.
        """
        config = {
            "notebook": TEST_FILES_PATH + "hw00.ipynb",
            "assignment_id": "hw00",
            "class_id": "some_class",
            "auth": "google",
            "save_environment": False,
            "ignore_modules": [],
            "endpoint": "http://some.url",
        }
        f = open(TEST_FILES_PATH + "demofile1.taeg", "a")
        f.write(json.dumps(config))
        f.close()
        g = open(TEST_FILES_PATH + "demofile2.taeg", "a")
        g.write(json.dumps(config))
        g.close()
        nb = nbformat.v4.new_notebook()
        text = """\
                        This is an auto-generated notebook."""
        nb['cells'] = [nbformat.v4.new_markdown_cell(text)]
        with open(TEST_FILES_PATH + 'test-nb.ipynb', "w") as f:
            nbformat.write(nb, f)
        grader = Notebook(TEST_FILES_PATH + "tests")
        self.assertRaises(ValueError,
                          lambda: grader.export(
                              nb_path=None, filtering=False))
        os.remove(TEST_FILES_PATH + "demofile1.taeg")
        os.remove(TEST_FILES_PATH + "demofile2.taeg")
        os.remove(TEST_FILES_PATH + "test-nb.ipynb")

    def test_export_multiple_taeg_error(self):
        """
        Checks export for error scenario for export method
        This test should pass when export successfully raises an
        AssertionError for the case when the directory contains
        multiple .taeg files.
        """
        grader = Notebook(TEST_FILES_PATH + "tests")
        self.assertRaises(ValueError,
                          lambda: grader.export(nb_path=None, filtering=False))

    @patch.object(LogEntry, "shelve")
    def test_nb_log(self, mock_log):
        """
        Checks existence of log when running nb
        """

        mock_log.return_value = LogEntry(EventType.CHECK)
        grader = Notebook(TEST_FILES_PATH + "tests")
        output = grader.check_all()

        self.assertTrue(os.path.isfile(_TAEG_LOG_FILENAME))

    def tearDown(self):
        for i in range(1, 7):
            file = "demofile{}.taeg".format(i)
            if os.path.isfile(file):
                os.remove(file)
        if os.path.isfile(_TAEG_LOG_FILENAME):
            os.remove(_TAEG_LOG_FILENAME)
        if os.path.exists("hw00.pdf"):
            os.remove("hw00.pdf")
        if os.path.exists("hw00.zip"):
            os.remove("hw00.zip")
