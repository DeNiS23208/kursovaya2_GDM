import pytest
from src.hh_api import HeadHunterAPI


@pytest.fixture
def hh_api():
    return HeadHunterAPI()


def test_get_vacancies(mocker, hh_api):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": [{"title": "Python Dev"}]}

    mocker.patch("requests.get", return_value=mock_response)

    vacancies = hh_api.get_vacancies("Python")
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Python Dev"


def test_get_vacancies_fail(mocker, hh_api):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.text = "Server error"

    mocker.patch("requests.get", return_value=mock_response)

    vacancies = hh_api.get_vacancies("Python")
    assert vacancies == []
