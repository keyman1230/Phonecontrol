import datetime


def return_now():
    now = datetime.datetime.now()

    return now.strftime("%Y-%m-%d_%H-%M-%S")
