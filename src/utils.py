import os

from src.jsonvacancystorage import JsonVacancyStorage
from src.settings import BASE_DIR

path = os.path.join(BASE_DIR, "data")
os.makedirs(path, exist_ok=True)     # Создаем директорию, если она не существует
file_path = os.path.join(path, "save_vacancies_json.json")

def user_interaction(hh_api):
    while True:
        print("\nДоступные команды:")
        print("1. Поиск вакансий по запросу")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Получить вакансии с ключевым словом в описании")
        print("4. Выход")

        choice = input("Выберите команду (1-4): ")

        if choice == '1':
            keyword = input("Введите поисковый запрос: ")
            vacancies = hh_api.load_vacancies(keyword)
            file_for_save = JsonVacancyStorage(file_path)
            if vacancies is not None and len(vacancies) != 0:
                print(f"Найдено {len(vacancies)} вакансий по запросу '{keyword}':")
                for vacancy in vacancies:
                    salary = vacancy.get('salary')  # Получаем объект зарплаты
                    salary_from = salary.get('from',
                                             'не указана') if salary else 'не указана'  # Проверяем, существует ли зарплата
                    print(f"- {vacancy['name']} (Зарплата: {salary_from})")
                    # Сохраняем результат в файле json в папке дата
                    file_for_save.add_vacancy(vacancy)

            else:
                print("Вакансии не найдены.")


        elif choice == '2':
            keyword = input("Введите поисковый запрос: ")
            vacancies = hh_api.load_vacancies(keyword)
            file_for_save = JsonVacancyStorage(file_path)

            if vacancies is not None and len(vacancies) > 0:
                n = int(input("Введите количество вакансий для отображения: "))

                # Фильтруем вакансии, чтобы оставить только те, у которых есть зарплата
                valid_vacancies = [
                    vacancy for vacancy in vacancies
                    if isinstance(vacancy, dict) and vacancy.get('salary') is not None]

                # Сортируем вакансии по зарплате
                sorted_vacancies = sorted(
                    valid_vacancies,
                    key=lambda x: (x['salary'].get('from') if x['salary'] else 0) or 0,
                    reverse=True)
                top_vacancies = sorted_vacancies[:n]

                print(f"Топ {n} вакансий по зарплате для запроса '{keyword}':")
                for vacancy in top_vacancies:
                    salary_from = vacancy['salary'].get('from', 'не указана')
                    print(f"- {vacancy['name']} (Зарплата: {salary_from})")
                    # Сохраняем результат в файле json в папке дата
                    file_for_save.add_vacancy(vacancy)


            else:
                print("Вакансии не найдены.")

        elif choice == '3':
            keyword = input("Введите ключевое слово для поиска в описании: ")
            vacancies = hh_api.load_vacancies(keyword)
            file_for_save = JsonVacancyStorage(file_path)

            if vacancies is not None and len(vacancies) > 0:
                # Фильтруем вакансии, чтобы оставить только те, у которых есть описание
                filtered_vacancies = [
                    vacancy for vacancy in vacancies
                    if isinstance(vacancy, dict)
                       and 'snippet' in vacancy
                       and vacancy['snippet'] is not None
                       and vacancy['snippet'].get('responsibility') is not None
                       and vacancy['snippet']['responsibility'].lower().find(keyword.lower()) != -1]

                if filtered_vacancies:
                    print(f"Вакансии с ключевым словом '{keyword}' в описании:")
                    for vacancy in filtered_vacancies:
                        salary_from = vacancy['salary'].get('from', 'не указана') if vacancy.get(
                            'salary') else 'не указана'
                        print(f"- {vacancy['name']} (Зарплата: {salary_from})")
                        # Сохраняем результат в файле json в папке дата
                        file_for_save.add_vacancy(vacancy)
                else:
                    print("Вакансии не найдены с указанным ключевым словом в описании.")


            else:
                print("Вакансии не найдены.")

        elif choice == '4':
            print("Выход из программы.")
            break

        else:
            print("Некорректный ввод. Пожалуйста, выберите команду от 1 до 4.")