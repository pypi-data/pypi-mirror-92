import ast
import astor
import pytest

from pytransformation import _make_for_loops_while
from .test_file_utilities import get_all_test_and_result_files

test_dir_name = "for_to_while"


@pytest.fixture(params=get_all_test_and_result_files(test_dir_name))
def test_and_result_strings(request):
    return request.param


def test_make_for_loops_while_loops(test_and_result_strings):
    test_string = test_and_result_strings[0]
    result_string = test_and_result_strings[1]

    test_ast = ast.parse(test_string)
    test_result_ast, _ = _make_for_loops_while(test_ast, {})
    test_result_string = astor.to_source(test_result_ast)

    assert(test_result_string == result_string)
