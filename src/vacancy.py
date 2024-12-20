class Vacancy:
    __slots__ = ['id', 'name', 'salary', 'url', 'employer', 'snippet']

    def __init__(self, id: str, name: str, salary: dict, url: str, employer: dict, snippet: dict):
        self.id = id
        self.name = name
        self.salary = self.validate_salary(salary)
        self.url = url
        self.employer = employer
        self.snippet = snippet

    def validate_salary(self, salary):
        """Валидирует значение зарплаты."""
        if salary is None:
            return 0

        if isinstance(salary, dict):
            if salary.get('from', 0) >= 0:
                return salary  # Возвращаем словарь, если он валиден
            else:
                return 0  # Если зарплата некорректная, возвращаем 0

        if isinstance(salary, (int, float)) and salary >= 0:
            return {"from": salary}  # Если это число, возвращаем его как словарь

        return 0

    def __lt__(self, other):
        """Метод сравнения для '<'."""
        return self.salary < other.salary

    def __le__(self, other):
        """Метод сравнения для '<='."""
        return self.salary <= other.salary

    def __eq__(self, other):
        """Метод сравнения для '=='."""
        return self.salary == other.salary

    def __gt__(self, other):
        """Метод сравнения для '>'."""
        return self.salary > other.salary

    def __ge__(self, other):
        """Метод сравнения для '>='."""
        return self.salary >= other.salary

    def __str__(self):
        """Возвращает строковое представление вакансии."""
        return f"Вакансия: {self.name}, Зарплата: {self.salary}, Ссылка: {self.url}, Описание: {self.snippet}"


