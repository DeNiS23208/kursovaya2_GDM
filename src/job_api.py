from abc import ABC, abstractmethod


class JobAPI(ABC):
    """Абстрактный класс для работы с API вакансий."""

    @abstractmethod
    def get_vacancies(self, keyword: str):
        """Метод для получения вакансий по ключевому слову."""
        pass
