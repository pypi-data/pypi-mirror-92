import json
import time
import hashlib
import datetime

def dump_json(data):
    return json.dumps(data, ensure_ascii=False)


def load_json(data):
    try:
        return json.loads(data)
    except:
        return None


def sleep(seconds):
    time.sleep(seconds)


def get_current_millisecond():
    return int(round(time.time() * 1000))


def get_current_second():
    return int(round(time.time()))


def md5(src):
    m2 = hashlib.md5()
    m2.update(src.encode())
    return m2.hexdigest()

def get_current_datetime():
    return datetime.datetime.now()