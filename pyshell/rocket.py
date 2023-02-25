import base64
import datetime
import random
import string
import time

from httprunner.exceptions import ParamsError


def get_random_string(str_len):
    """ generate random string with specified length
    """
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(str_len)
    )


def get_timestamp(str_len=13):
    """ get timestamp string, length can only between 0 and 16
    """
    if isinstance(str_len, int) and 0 < str_len < 17:
        return str(time.time()).replace(".", "")[:str_len]
    raise ParamsError("timestamp length can only between 0 and 16.")


def sleep(n_secs):
    """ sleep n seconds
    """
    time.sleep(n_secs)


def get_random_number(a, b):
    """get a number between a and b
    """
    if isinstance(a, int) and isinstance(b, int):
        return random.randint(a, b)
    raise ParamsError("a or b type can only int.")


def get_current_time():
    """get current date, default format is %Y-%m-%d %H:%M:%S
    """
    return time.strftime("%Y-%m-%d %H:%M:%S")


def get_now_plus_time(unit, number):
    """compute time: now add some time, support: days, hours, minutes, seconds
    """
    fmt = "%Y-%m-%d %H:%M:%S"
    if unit == "days":
        return (datetime.datetime.now() + datetime.timedelta(days=number)).strftime(fmt)
    elif unit == "hours":
        return (datetime.datetime.now() + datetime.timedelta(hours=number)).strftime(fmt)
    elif unit == "minutes":
        return (datetime.datetime.now() + datetime.timedelta(minutes=number)).strftime(fmt)
    elif unit == "seconds":
        return (datetime.datetime.now() + datetime.timedelta(seconds=number)).strftime(fmt)
    else:
        return "unit must in [days, hours, minutes, seconds]"


def get_now_reduce_time(unit, number):
    """compute time: now reduce some time, support: days, hours, minutes, seconds
    """
    fmt = "%Y-%m-%d %H:%M:%S"
    if unit == "days":
        return (datetime.datetime.now() - datetime.timedelta(days=number)).strftime(fmt)
    elif unit == "hours":
        return (datetime.datetime.now() - datetime.timedelta(hours=number)).strftime(fmt)
    elif unit == "minutes":
        return (datetime.datetime.now() - datetime.timedelta(minutes=number)).strftime(fmt)
    elif unit == "seconds":
        return (datetime.datetime.now() - datetime.timedelta(seconds=number)).strftime(fmt)
    else:
        return "unit must in [days, hours, minutes, seconds]"


def get_base64_encode(variable):
    """base64 encode
    """
    _variable = str(variable).encode()
    return base64.b64encode(_variable).decode()
