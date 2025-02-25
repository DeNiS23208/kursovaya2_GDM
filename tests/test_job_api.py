import pytest
from src.job_api import JobAPI


def test_job_api_abstract():
    with pytest.raises(TypeError):
        JobAPI()
