import json
import os
from abc import ABC, abstractmethod
from typing import List


class Vacancy:
    def __init__(self, title: str, url: str, salary: str, description: str) -> None:
        self.title: str = title
        self.url: str = url
        self.salary: str = salary
        self.description: str = description

    def __lt__(self, other):
        # Если оба объекта - вакансии, сравниваем их зарплаты
        if isinstance(other, Vacancy):
            return self.salary < other.salary
        return False  # Если объект не вакансия, возвращаем False

    def to_dict(self) -> dict[str, str]:
        return {
            "title": self.title,
            "url": self.url,
            "salary": self.salary,
            "description": self.description,
        }


class FileSaver(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class VacancySaver:
    def __init__(self, filename: str = "data/vacancies.json") -> None:
        # Абсолютный путь к файлу
        self.filename: str = os.path.abspath(filename)

        self.vacancies: List[dict[str, str]] = []

        # Создаем папку, если её нет
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        # Загружаем данные из файла, если он существует
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                self.vacancies = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # Игнорируем ошибку, если файла нет или он пустой

    def add_vacancy(self, vacancy: Vacancy) -> None:
        self.vacancies.append(vacancy.to_dict())
        self._save_to_file()

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        self.vacancies = [
            v for v in self.vacancies if v["url"] != vacancy.url
        ]  # Используем 'url' как уникальный идентификатор
        self._save_to_file()

    def _save_to_file(self) -> None:
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.vacancies, file, ensure_ascii=False, indent=4)

    def get_vacancies(self) -> List[dict[str, str]]:
        return self.vacancies
