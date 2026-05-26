class EResult:
    """Цифровые коды ответов в стиле Valve/Steam (EResult)"""

    OK = 1  # Полный успех операции
    FAIL = 2
    PENDING = 2  # Ожидание действия (например, клика по ссылке)
    HANDSHAKE_ERROR = 36
    INVALID_TOKEN = 14  # Неверный токен или сессия
    DUPLICATE_NAME = 20  # Такое имя аккаунта уже занято
    EXPIRED = 42  # Время жизни ссылки или сессии вышло
    CAPTCHA_FAILED = 85  # Робот не прошёл проверку капчи
