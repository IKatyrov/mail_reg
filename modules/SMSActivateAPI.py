import json
import time
import requests

class SMSActivateAPI:
    # Определяем базовый URL-адрес до API
    __base_url = "https://sms-activate.ru/stubs/handler_api.php"
    # Инициализируем API-ключ
    def __init__(self, api_key):
        self.__api_key = api_key
    # Получить баланс
    def get_balance(self):
        # Определяем параметры запроса
        params = {
        "api_key": self.__api_key,
        "action": "getBalance",
        }
        # Отправляем запрос на сервер
        res = requests.post(self.__base_url, params=params)
        # Если пришёл положительный ответ
        if res.status_code == 200:
            # Возвращаем значение
            # Ответ приходет в формате вида ACCESS_BALANCE:'баланс на счету'
            # Разбивем его по символу ":" и возвращаем числовое значение
            return float(res.text.split(":")[1])
        # В противном случае возвращаем статус-код
        return res.status_code

    # Получить количество свободных номеров
    def get_numbers_status(self, country=None, operator=None):
        # Определяем параметры запроса
        params = {
        "api_key": self.__api_key,
        "action": "getNumbersStatus",
        "country": country,
        "operator": operator,
        }
        # Отправляем запрос на сервер
        res = requests.post(self.__base_url, params=params)
        # Если пришёл положительный ответ
        if res.status_code == 200:
            # Возвращаем значение
            return json.loads(res.text)
        # В противном случае возвращаем статус-код
        return res.status_code
        # Заказать номер
    def get_number(self, service, operator="any", forward=0, country=0):
        # Определяем параметры запроса
        params = {
        "api_key": self.__api_key,
        "action": "getNumber",
        "service": service,
        "operator": operator,
        "forward": forward,
        "country": country,
        }
        # Отправляем запрос на сервер
        res = requests.post(self.__base_url, params=params)
        # Если пришёл положительный ответ
        if res.status_code == 200 and "ACCESS_NUMBER" in res.text:
            # Возвращаем номер
            # Ответ приходет в формате вида ACCESS_NUMBER:$id:$number , где ($id - id операции,$number - номер телефона)
            # Разбивем его по символу ":" и возвращаем список ез первого элемента
            list = res.text.split(":")[1:3]
            return list
    # Установить статус
    def set_status(self, activation_id, status, forward=0):
        # Определяем параметры запроса
        params = {
        "api_key": self.__api_key,
        "id": activation_id,
        "status": status,
        "action": "setStatus",
        }
        # Отправляем запрос на сервер
        res = requests.post(self.__base_url, params=params)
        # Если пришёл положительный ответ
        if res.status_code == 200:
            # Возвращаем значение
            return res.text
        # Иначе, возвращаем код ответа
        return res.status_code
    # Получить статус
    def get_status(self, activation_id):
        # Определяем параметры запроса
        params = {
        "api_key": self.__api_key,
        "id": activation_id,
        "action": "getStatus",
        }
        # Отправляем запрос на сервер
        res = requests.post(self.__base_url, params=params)
        # Если пришёл положительный ответ
        if res.status_code == 200:
            # Возвращаем значение
            return res.text.split(":")
        # Иначе, возвращаем код ответа
        return res.status_code

    # Получаем код
    def get_code(self, id, wait=3, max_wait=60):
        # Инициализируем счётчик времени
        wait_time = 0
        # Получаем статус СМС
        status = self.get_status(id)
        # Если код был прислан
        # Иначе, запускаем цикл для ожидания СМС кода
        for i in range(max_wait):
            # Получаем статус СМС
            status = self.get_status(id)
            print(status[0])
            # Если код был прислан
            if "STATUS_OK" in status:
                # Возвращаем код
                return status
            # Ожидаем 1 секунду
            time.sleep(wait)
            # Увеличиваем счётчик ожидания
            wait_time += wait
            # Если время, которое мы прождали больше,
            # либо равно максимально допустимому времени
            # ожидания, тогда возвращаем None
            if wait_time >= max_wait:
                print(f"Timeout: {max_wait} seconds")
                # Возвращаем None
                return None