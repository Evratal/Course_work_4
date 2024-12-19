from src.hh import HH


if __name__ == "__main__":
    hh_api = HH()  # Создаем экземпляр класса HH
    hh_api.connect()  # Подключаемся к API
    hh_api.user_interaction()  # Запускаем взаимодействие с пользователем
