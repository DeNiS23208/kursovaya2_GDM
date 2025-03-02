import json
import os
import pytest
from src.vacancy_saver import Vacancy, VacancySaver


@pytest.fixture
def vacancy():
    return Vacancy(
        title="Программист Python",
        url="https://example.com/vacancy1",
        salary=100000,
        description="Разработка на Python",
    )


@pytest.fixture
def vacancy_saver():
    test_file = "tests/test_vacancies.json"
    if os.path.exists(test_file):
        os.remove(test_file)
    return VacancySaver(test_file)


def test_vacancy_creation(vacancy):
    assert vacancy.title == "Программист Python"
    assert vacancy.url == "https://example.com/vacancy1"
    assert vacancy.salary == 100000.0
    assert vacancy.description == "Разработка на Python"


def test_vacancy_invalid_url():
    with pytest.raises(ValueError, match="Ссылка должна начинаться с https://"):
        Vacancy("Invalid", "http://example.com", 50000, "Ошибка")


def test_vacancy_comparison():
    v1 = Vacancy("Python Dev", "https://url1.com", 90000, "Desc")
    v2 = Vacancy("Java Dev", "https://url2.com", 120000, "Desc")
    assert v1 < v2


def test_add_vacancy(vacancy_saver, vacancy):
    vacancy_saver.add_vacancy(vacancy)

    with open(vacancy_saver.filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert len(data) == 1
    assert data[0]["title"] == vacancy.title


def test_delete_vacancy(vacancy_saver, vacancy):
    vacancy_saver.add_vacancy(vacancy)
    vacancy_saver.delete_vacancy(vacancy)

    with open(vacancy_saver.filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert len(data) == 0
