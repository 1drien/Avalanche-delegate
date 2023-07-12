import pytest


@pytest.fixture(autouse=True)
def isolation(
    fn_isolation,
):  # TO BE REPLACED BY py_vector.common.testing simple_isolation if issues
    pass
