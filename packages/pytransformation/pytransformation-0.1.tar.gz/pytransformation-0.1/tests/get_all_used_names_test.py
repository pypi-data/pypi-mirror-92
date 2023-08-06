import ast
import pytest

from pytransformation import _get_all_used_variable_names
from .test_file_utilities import get_all_test_and_result_files

test_dir_name = "get_all_used_names"


@pytest.fixture(params=get_all_test_and_result_files(test_dir_name))
def test_and_result_strings(request):
    return request.param


def test_get_all_names_gets_all_names_used(test_and_result_strings):
    test_string = test_and_result_strings[0]
    test_ast = ast.parse(test_string)

    names_used = {
        'ast': None,
        'func': None,
        'x': None,
        'len_x': None,
        'y': None,
        'len': None,
        'z': None,
        'z2': None,
        'z3': None
    }
    assert(_get_all_used_variable_names(test_ast) == names_used)
