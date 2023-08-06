import ast
import astor
import pytest

from pytransformation import _name_unnamed_applications
from .test_file_utilities import get_all_test_and_result_files

test_dir_name = "name_func_apps"


@pytest.fixture(params=get_all_test_and_result_files(test_dir_name))
def test_and_result_strings(request):
    return request.param


def test_name_func_apps(test_and_result_strings):
    test_string = test_and_result_strings[0]
    result_string = test_and_result_strings[1]

    test_ast = ast.parse(test_string)
    if isinstance(test_ast.body[0], ast.FunctionDef):
        test_ast = test_ast.body[0]
    test_result_ast, _ = _name_unnamed_applications(test_ast, {})
    test_result_string = astor.to_source(test_result_ast)

    assert(test_result_string == result_string)
