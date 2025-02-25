import json
import os
from abc import ABC, abstractmethod
from typing import List


class Vacancy:
    __slots__ = ("title", "url", "salary", "description")

    def __init__(self, title: str, url: str, salary: float, description: str):
        self.title = title
        self.url = url
        self.salary = self._parse_salary(salary)
        self.description = description
        self._validate_data()

    def _parse_salary(self, salary):
        if isinstance(salary, dict):  # Если зарплата передана как словарь
            return 0.0
        return salary if salary and salary > 0 else 1.0

    def _validate_data(self):
        if self.salary < 0:
            raise ValueError("Зарплата должна быть неотрицательной")

        if not self.url.startswith("https://"):
            raise ValueError("Ссылка должна начинаться с https://")

    def __lt__(self, other):
        return isinstance(other, Vacancy) and self.salary < other.salary

    def to_dict(self) -> dict[str, str | float]:
        return {
            "title": self.title,
            "url": self.url,
            "salary": self.salary,
            "description": self.description,
        }


class FileSaver(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy):
        pass

    @abstractmethod
    def get_vacancies(self) -> List[dict[str, str | float]]:
        pass


class VacancySaver(FileSaver):
    def __init__(self, filename: str = "data/vacancies.json") -> None:
        self.filename: str = os.path.abspath(filename)
        self.vacancies: List[dict[str, str | float]] = []
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                self.vacancies = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def add_vacancy(self, vacancy: Vacancy) -> None:
        self.vacancies.append(vacancy.to_dict())
        self._save_to_file()

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        self.vacancies = [v for v in self.vacancies if v["url"] != vacancy.url]
        self._save_to_file()

    def _save_to_file(self) -> None:
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.vacancies, file, ensure_ascii=False, indent=4)

    def get_vacancies(self) -> List[dict[str, str | float]]:
        return self.vacancies
