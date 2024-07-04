import secrets
import string


def randomStr(length:int=8):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

if __name__ == "__main__":
    print(randomStr())