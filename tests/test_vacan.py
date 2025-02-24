import json
import os
import sys

import pytest

from src.vacancy_saver import Vacancy, VacancySaver

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "service"))
)


# Фикстура для создания объекта VacancySaver
@pytest.fixture
def vacancy_saver():
    file_path = os.path.join(os.path.dirname(__file__), "test_vacancies.json")
    # Удаляем файл перед тестами, чтобы он был пустым
    if os.path.exists(file_path):
        os.remove(file_path)
    return VacancySaver(file_path)


# Фикстура для создания данных вакансии
@pytest.fixture
def vacancy_data():
    return Vacancy(
        title="Программист Python",
        url="https://example.com/vacancy1",
        salary="100000",
        description="Разработка на Python",
    )


# Тест: добавление вакансии в пустой файл
def test_add_vacancy(vacancy_saver, vacancy_data):
    vacancy_saver.add_vacancy(vacancy_data)

    # Проверяем, что файл существует
    file_path = os.path.join(os.path.dirname(__file__), "test_vacancies.json")
    assert os.path.exists(file_path), "Файл не был создан."

    # Читаем содержимое файла
    with open(file_path, "r", encoding="utf-8") as f:
        data_written = f.read()

    # Ожидаемые данные, которые должны быть записаны в файл
    expected_data = [
        {
            "title": "Программист Python",
            "url": "https://example.com/vacancy1",
            "salary": "100000",
            "description": "Разработка на Python",
        }
    ]

    # Проверяем, что данные в файле соответствуют ожидаемым
    vacancies = json.loads(data_written)
    assert (
        vacancies == expected_data
    ), f"Ожидалось: {expected_data}, но получено: {vacancies}"

    os.remove(file_path)


# Тест: добавление вакансий в уже существующий файл
def test_add_vacancy_to_existing_file(vacancy_saver, vacancy_data):
    # Добавляем первую вакансию
    vacancy_saver.add_vacancy(vacancy_data)

    # Добавляем вторую вакансию
    vacancy2 = Vacancy(
        title="Программист Java",
        url="https://example.com/vacancy2",
        salary="120000",
        description="Разработка на Java",
    )
    vacancy_saver.add_vacancy(vacancy2)

    # Проверяем, что файл существует
    file_path = os.path.join(os.path.dirname(__file__), "test_vacancies.json")
    assert os.path.exists(file_path), "Файл не был создан."

    # Читаем содержимое файла
    with open(file_path, "r", encoding="utf-8") as f:
        data_written = f.read()

    # Ожидаемые данные, которые должны быть записаны в файл
    expected_data = [
        {
            "title": "Программист Python",
            "url": "https://example.com/vacancy1",
            "salary": "100000",
            "description": "Разработка на Python",
        },
        {
            "title": "Программист Java",
            "url": "https://example.com/vacancy2",
            "salary": "120000",
            "description": "Разработка на Java",
        },
    ]

    # Проверяем, что данные в файле соответствуют ожидаемым
    vacancies = json.loads(data_written)
    assert (
        vacancies == expected_data
    ), f"Ожидалось: {expected_data}, но получено: {vacancies}"

    os.remove(file_path)


# Тест: проверка формата данных в файле
def test_data_format_in_file(vacancy_saver, vacancy_data):
    vacancy_saver.add_vacancy(vacancy_data)

    # Проверяем, что файл существует
    file_path = os.path.join(os.path.dirname(__file__), "test_vacancies.json")
    assert os.path.exists(file_path), "Файл не был создан."

    # Читаем содержимое файла
    with open(file_path, "r", encoding="utf-8") as f:
        data_written = f.read()

    # Проверяем, что данные соответствуют формату JSON
    try:
        vacancies = json.loads(data_written)
    except json.JSONDecodeError as e:
        pytest.fail(f"Неверный формат данных в файле: {e}")

    # Проверяем, что вакансии содержат необходимые поля
    assert isinstance(vacancies, list), "Данные в файле должны быть списком"
    assert all(
        "title" in vacancy
        and "url" in vacancy
        and "salary" in vacancy
        and "description" in vacancy
        for vacancy in vacancies
    ), "Каждая вакансия должна содержать поля 'title', 'url', 'salary', 'description'"

    os.remove(file_path)


# Тест: восстановление данных после перезапуска
def test_load_vacancies_after_restart(vacancy_saver, vacancy_data):
    vacancy_saver.add_vacancy(vacancy_data)

    # Перезапускаем объект VacancySaver (воссоздаем объект, как если бы программа перезапустилась)
    file_path = os.path.join(os.path.dirname(__file__), "test_vacancies.json")
    vacancy_saver2 = VacancySaver(file_path)

    # Проверяем, что вакансии были загружены
    assert (
        len(vacancy_saver2.vacancies) == 1
    ), f"Ожидалось 1 вакансию, но получено {len(vacancy_saver2.vacancies)}"
    assert (
        vacancy_saver2.vacancies[0]["title"] == "Программист Python"
    ), "Загруженная вакансия имеет неверное название"

    os.remove(file_path)
