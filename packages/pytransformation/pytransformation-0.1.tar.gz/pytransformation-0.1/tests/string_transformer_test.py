import pytest

from pytransformation import String_Transformer
from pytransformation import Transformations
from .test_file_utilities import get_all_test_and_result_files


test_dir_name = "string_transformer"


@pytest.fixture(params=get_all_test_and_result_files(test_dir_name))
def test_and_result_strings(request):
    return request.param


@pytest.fixture(scope="function")
def transformer_and_mocks(mocker):
    mock1 = mocker.spy(Transformations, "MOVE_DECLS_TO_TOP_OF_SCOPE")
    mock2 = mocker.spy(Transformations, "MAKE_FOR_LOOPS_WHILE")
    mock3 = mocker.spy(Transformations, "NAME_ALL_FUNCTION_APPLICATIONS")

    transformer = String_Transformer([
        Transformations.MAKE_FOR_LOOPS_WHILE,
        Transformations.MOVE_DECLS_TO_TOP_OF_SCOPE,
        Transformations.NAME_ALL_FUNCTION_APPLICATIONS,
    ])
    return (transformer, (mock1, mock2, mock3))


def test_SCT_calls_transfroms_correct_num_times(mocker,
                                                transformer_and_mocks,
                                                test_and_result_strings):

    transformer = transformer_and_mocks[0]
    transformer.transform(test_and_result_strings[0])
    mocks = transformer_and_mocks[1]
    # First test file has 4 functions in one module, so 5 scope opening
    # objects, so all transforms should be called 5 times.
    for mock in mocks:
        assert mock.call_count == 5


def test_SCT_resets_name_dict_after_transforming(transformer_and_mocks,
                                                 test_and_result_strings):
    transformer = transformer_and_mocks[0]
    assert transformer._names_in_use == {}
    transformer.transform(test_and_result_strings[0])
    assert transformer._names_in_use == {}
