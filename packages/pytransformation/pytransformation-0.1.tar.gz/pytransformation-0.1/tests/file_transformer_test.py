import os
import pytest

from pytransformation import File_Transformer
from pytransformation import Transformations


test_dir_name = "file_transformer"


@pytest.fixture(scope="function")
def transformer():
    transformer = File_Transformer([
        Transformations.MAKE_FOR_LOOPS_WHILE,
        Transformations.MOVE_DECLS_TO_TOP_OF_SCOPE,
        Transformations.NAME_ALL_FUNCTION_APPLICATIONS,
    ])
    return transformer


def test_file_transformer_writes_to_file(transformer):
    absolute_path = os.path.dirname(os.path.realpath(__file__))
    test_dir = os.path.join(absolute_path, "test_files", test_dir_name)
    in_file = os.path.join(test_dir, "testcase_1.py")
    out_file = "test_out_file.py"

    transformer.transform(in_file, out_file)

    is_out_file_created = os.path.isfile(out_file)

    assert is_out_file_created

    os.remove(out_file)
