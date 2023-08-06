from pytransformation import _new_name


def test_get_new_name_does_not_dupclicate_names():
    name = 'x'
    names_already_used = ['x', 'x0', 'x1']
    assert(_new_name(name, names_already_used) == 'x2')
