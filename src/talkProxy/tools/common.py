import logging
import secrets
import string
import time

def randomStr(length:int=8):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def timestamp():
    return int(time.time())

def passtimes(time1: int, time2: int) -> int:
    try:
        return time2 - time1
    except Exception as e:
        logging.error(f"时间戳计算失败:{e}")
        return None
    

if __name__ == "__main__":
    print(randomStr())