import requests

from src.job_api import JobAPI


class HeadHunterAPI(JobAPI):
    """Класс для работы с API HeadHunter."""

    BASE_URL: str = "https://api.hh.ru/vacancies"

    def _connect_to_api(self, params: dict) -> requests.Response:
        """Подключение к API."""
        response = requests.get(self.BASE_URL, params=params)
        return response

    def get_vacancies(self, keyword: str) -> list[dict]:
        """Получает вакансии по ключевому слову."""
        params = {"text": keyword, "per_page": 20}  # Ограничим 20 вакансиями для теста
        response = self._connect_to_api(params)

        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            return []
