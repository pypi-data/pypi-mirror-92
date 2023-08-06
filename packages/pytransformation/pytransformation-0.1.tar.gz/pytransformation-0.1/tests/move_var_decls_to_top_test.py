import ast
import astor
import pytest

from pytransformation import _move_var_decls_to_top_of_scope
from .test_file_utilities import get_all_test_and_result_files

test_dir_name = "move_var_decls"


@pytest.fixture(params=get_all_test_and_result_files("move_var_decls"))
def test_and_result_strings(request):
    return request.param


def test_move_var_decls_to_top(test_and_result_strings):
    test_string = test_and_result_strings[0]
    result_string = test_and_result_strings[1]

    test_ast = ast.parse(test_string)
    if isinstance(test_ast.body[0], ast.FunctionDef):
        test_ast = test_ast.body[0]
    test_result_ast, _ = _move_var_decls_to_top_of_scope(test_ast, {})
    test_result_string = astor.to_source(test_result_ast)

    assert(test_result_string == result_string)
