import time
from modules.SMSActivateAPI import SMSActivateAPI
from selenium.common.exceptions import NoSuchElementException

class MailReg:
    def __init__(self, chrome_driver, sms_activate_key):
        # Инициализируем объект chrome-драйвера
        self.__chrome_driver = chrome_driver
        # Инициализируем объект SMS-активации
        self.__sms_activate = SMSActivateAPI(sms_activate_key)

    def close_browser(self):
        # Закрываем драйвер
        self.__chrome_driver.close()

    def __check_exists_by_css(self, css_selector):
        try:
            # Пробуем найте элемент
            print(f"Ищем элемент: {css_selector}")
            self.__chrome_driver.find_element_by_css_selector(css_selector)
        except NoSuchElementException:
            # Если элемента на странице нет - возвращаем False
            print(f"Элемент: {css_selector} Не найден!")
            return False
        # Иначе возвращаем True
        return True

    # Ищем элемент в течении заданного времени
    def __find_and_wait(self, css_selector, wait_time=60):
        # Запускаем цикл, по количеству секунд ожидания
        for i in range(wait_time):
            # Если элемент найден -- возвращаем его
            if self.__check_exists_by_css(css_selector):
                return self.__chrome_driver.find_elements_by_css_selector(css_selector)
            # Иначе -- ждём 1 секунду
            else:
                time.sleep(1)
    def __check_exists_by_css_in_element(self, element, css_selector):
        try:
            # Пробуем найте элемент
            element.find_element_by_css_selector(css_selector)
        except NoSuchElementException:
            # Если элемента на странице нет - возвращаем False
            return False
        # Иначе возвращаем True
        return True
    def __find_and_wait_in_element(self, element, css_selector, wait_time=60):
        for i in range(wait_time):
            # Если элемент найден -- возвращаем его
            if self.__check_exists_by_css_in_element(element, css_selector):
                return element.find_elements_by_css_selector(css_selector)
            # Иначе -- ждём 1 секунду
            else:
                time.sleep(1)
    def __input(self, value, css_selector, position=0):
        # Ищем элемент
        input = self.__find_and_wait(css_selector)
        # Кликаем по инпуту
        input[position].click()
        # Вводим логин в форму
        input[position].send_keys(value)
    def __click(self, css_selector, position=0):
        # Ищем элемент
        elem = self.__find_and_wait(css_selector)
        # Кликаем по инпуту
        elem[position].click()
    def __go_to_page(self):
        # Переходим на страницу регистрации
        self.__chrome_driver.get("https://account.mail.ru/signup?from=main&rf=auth.mail.ru")
    def __input_name(self, name):
        # Вводим имя пользователя
        self.__input(name, "input#fname")
    def __input_surname(self, lname):
        # Вводим фамилию пользователя
        self.__input(lname, "input#lname")
    def __input_birth_day(self, day):
        # Открываем список дней
        self.__find_and_wait("div[data-test-id='birth-date__day']")[0].click()
        # Получаем список дней
        list_of_days = self.__find_and_wait("div.Select-menu-outer")[0]
        days = self.__find_and_wait_in_element(list_of_days, "div.Select-option")
        # Кликаем по заданному дню
        days[day-1].click()
    def __input_birth_month(self, month):
        # Открываем список месяцев
        self.__find_and_wait("div[data-test-id='birth-date__month']")[0].click()
        # Получаем список месяцев
        list_of_days = self.__find_and_wait("div.Select-menu-outer")
        days = self.__find_and_wait_in_element(list_of_days[0], "div.Select-option")
        # Выбираем соответствующий месяц
        days[month-1].click()
    def __input_birth_year(self, year):
        # Открываем список по годам
        self.__find_and_wait("div[data-test-id='birth-date__year']")[0].click()
        # Получаем список по годам
        list_of_days = self.__find_and_wait("div.Select-menu-outer")
        days = self.__find_and_wait_in_element(list_of_days[0], "div.Select-option")
        # Выбираем нужный год. 1 - 2020, 2 - 2019, 3 - 2018 и т.д.
        days[year-1].click()
    def __input_sex(self, sex):
        # Если пол равен 0
        if sex:
            # Выбираем мужской
            self.__find_and_wait("label[data-test-id='gender-male']")[0].click()
        # Иначе
        else:
            # Выбираем женский
            self.__find_and_wait("label[data-test-id='gender-female']")[0].click()
    def __input_login(self, login):
        # Вводим логин
        self.__input(login, "input#aaa__input")
    def __input_password(self, password):
        # Вводим пароль
        self.__input(password, "input#password")
    def __input_repeat_password(self, password):
        # Повторяем ввод пароля
        self.__input(password, "input#repeatPassword")
    def __get_num(self):
        # Получаем статистику по свободным номерам
        count_of_num = self.__sms_activate.get_numbers_status(country=0, operator="any")
        # Узнаём баланс
        balance = self.__sms_activate.get_balance()
        # Если номера для заданного сервиса есть
        if int(count_of_num["ma_0"]) > 0 and balance >= 1:
            # Заказываем номер
            return self.__sms_activate.get_number("ma", "any")
    def __input_phone(self, phone):
        # Вводим номер телефона для активации
        self.__input(phone, "input#phone-number__phone-input")
    def __send_form(self):
        # Отправляем форму
        self.__click("button[data-test-id='first-step-submit']")
    def __take_sms_code(self):
        # Ожидаем пока появится кнопка для получения СМС
        self.__find_and_wait("a[data-test-id='resend-callui-link']", wait_time=250)[0].click()
    def __input_code(self, code):
        # Вводим код из СМС
        self.__input(code, "input[data-test-id='code']")
    def __send_code(self):
        # Отправляем код на сервер
        self.__click("button[data-test-id='verification-next-button'")
    def __input_base_form(self, user):
        # Переходим на страницу регистрации
        self.__go_to_page()
        # Вводим имя
        self.__input_name(user.name)
        # Вводим фамилию
        self.__input_surname(user.surname)
        # Вводим день рождения
        1*8*1*8*5
        self.__input_birth_day(user.birth_day)
        # Вводим месяц рождения
        self.__input_birth_month(user.birth_month)
        # Вводим год рождения
        self.__input_birth_year(user.age)
        # Выбираем пол
        self.__input_sex(user.sex)
        # Вводим логин
        self.__input_login(user.login)
        # Вводим пароль
        self.__input_password(user.password)
        # Повторяем ввод пароля
        self.__input_repeat_password(user.password)
    def __set_phone(self):
        # Получаем номер
        num = self.__get_num()
        # Вводим номер телефона
        self.__input_phone(num[1][1::])
        # Отправляем форму
        self.__send_form()
        # Просим mail.ru отправить код по СМС
        self.__take_sms_code()
        return num
    def __confirm_phone(self, id):
        # Указываем, что код отправлен
        self.__sms_activate.set_status(id, 1)
        # Ждём прихода СМС-кода
        code = self.__sms_activate.get_code(id, max_wait=250)
        # Если код успешно вернулся
        if code is not None and code[0] == "STATUS_OK":
            # Вводим код
            self.__input_code(code[1])
            # Уведомляем сервис о том, что код получен
            self.__sms_activate.set_status(id, status=6)
            # Отправляем код подтверждения mail.ru
            self.__send_code()
    def reg(self, user):
        # Заполняем форму регистрации
        self.__input_base_form(user)
        # Вводим номер телефона в форму
        num = self.__set_phone()
        # Подтверждаем регистрацию по СМС
        self.__confirm_phone(num[0])