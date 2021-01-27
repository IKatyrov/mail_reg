from modules.MailReg import MailReg
from modules.User import User
from selenium.webdriver import Chrome

# Создаём объект браузера
chrome_obj = Chrome(executable_path="assets/drivers/chromedriver.exe")
# Объявляем API-ключ сервиса СМС-активации
sms_api_key = "A764A0Ad1412340f181c786240b53c4d"

# Создаём объект с данными пользователя для регистрации
user = User(
    name="Марк",
    surname="Аврелий",
    sex=True,
    login="Логин",
    password="Пароль",
    birth_day=18,
    birth_month=8,
    age=2
)
try:
    # Создаём объект регистратора почты
    mail_reg = MailReg(chrome_obj, sms_api_key)
    # Запускаем процесс регистрации
    mail_reg.reg(user)
finally:
    mail_reg.close_browser()