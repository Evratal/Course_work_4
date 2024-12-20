from src.hh import HH
from src.utils import user_interaction

if __name__ == "__main__":
    hh_api = HH()  # Создаем экземпляр класса HH
    hh_api.connect()  # Подключаемся к API
    user_interaction(hh_api)  # Запускаем взаимодействие с пользователем
