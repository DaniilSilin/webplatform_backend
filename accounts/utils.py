import secrets

def generate_random_numbers() -> str:
    code = str(secrets.randbelow(900000) + 100000)
    return code