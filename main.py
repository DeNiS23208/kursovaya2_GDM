from src.hh_api import HeadHunterAPI
from src.vacancy_saver import Vacancy, VacancySaver


def main(vacancy_saver: VacancySaver) -> None:
    hh_api: HeadHunterAPI = HeadHunterAPI()

    keyword: str = input("Введите ключевое слово для поиска вакансий: ")
    vacancies: list[dict] = hh_api.get_vacancies(keyword)

    if not vacancies:
        print("Вакансии не найдены.")
        return

    print(f"Найдено {len(vacancies)} вакансий:")
    for vacancy in vacancies:
        print(f"{vacancy['name']} - {vacancy['alternate_url']}")

    # Сохранение вакансий в JSON
    for vacancy in vacancies:
        vacancy_obj: Vacancy = Vacancy(
            title=vacancy["name"],
            url=vacancy["alternate_url"],
            salary=vacancy.get("salary", "Не указана"),
            description=vacancy.get("snippet", {}).get("requirement", "Нет описания"),
        )
        vacancy_saver.add_vacancy(vacancy_obj)

    print("Вакансии сохранены в файл.")


if __name__ == "__main__":
    vacancy_saver: VacancySaver = VacancySaver(
        "data/vacancies.json"
    )  # Создаём только один раз
    main(vacancy_saver)  # Передаём его в `main()`
