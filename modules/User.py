class User:
    def __init__(self, name, surname, sex, login, password, birth_day, birth_month, age):
        # Имя
        self.name = name
        # Фамилия
        self.surname = surname
        # Пол. True - мужской, False - женский
        self.sex = sex
        # Логин
        self.login = login
        # Пароль
        self.password = password
        # День рождения
        self.birth_day = birth_day
        # Месяц рождения
        self.birth_month = birth_month
        # Год рождения.
        self.age = age