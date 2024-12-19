import json
import os

from src.settings import BASE_DIR


class SaveJson:
    def __init__(self,data):
        self.data = data


    def to_json(self):
        # Сериализация данных в строку JSON с параметрами для улучшения читаемости
        return json.dumps(self.data, ensure_ascii=False, indent=4)

    def save_file(self):
        path = os.path.join(BASE_DIR, "data")
        os.makedirs(path, exist_ok=True)     # Создаем директорию, если она не существует
        file_path = os.path.join(path, "save_vacancies_json.json")  # Добавляем расширение .json

        # Записываем данные в файл
        with open(file_path,"w", encoding='utf8') as file:
            file.write(self.to_json())

        try:
            with open(file_path, "w", encoding='utf8') as file:
                file.write(self.to_json())
            print(f"Данные успешно сохранены в {file_path}")
        except Exception as excep:
            print(f"Ошибка при сохранении файла: {excep}")

        @staticmethod
        def load_file():
            file_path = os.path.join(BASE_DIR, "data", "save_vacancies_json.json")
            try:
                with open(file_path, "r", encoding='utf8') as file:
                    data = json.load(file)
                return data
            except FileNotFoundError:
                print("Файл не найден.")
                return None
            except json.JSONDecodeError:
                print("Ошибка при декодировании JSON.")
                return None
            except Exception as e:
                print(f"Ошибка при загрузке файла: {e}")
                return None