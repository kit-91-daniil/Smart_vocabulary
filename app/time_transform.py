def seconds_to_russian_string(seconds: int) -> str:
    """
    :param seconds:
    :return: rest time russian string
    1 month - 3600*24*30 = 2 592 000 seconds
    1 day - 3600*24 = 86 400 seconds
    1 hour - 3600 seconds
    """
    abs_seconds = abs(seconds)
    days = (abs_seconds % (3600*24*30))//(3600*24)
    hours = (abs_seconds % 86400) // 3600
    minutes = (abs_seconds % 3600) // 60
    month_str = "1 месяц " if abs_seconds > 2592000 else ""
    days_str = (str(days) + days_string(days)) if days else ""
    hours_str = (str(hours) + hours_string(hours)) if hours else ""
    minutes_str = (str(minutes) + minutes_string(minutes)) if minutes else ""
    res_str = f"{month_str}{days_str}{hours_str}{minutes_str}"
    return res_str


def days_string(days_number: int) -> str:
    """
    :param days_number: days quantity
    :return: russian quantity days string
    """
    if days_number % 10 == 1 and days_number != 11:
        return " день "
    elif days_number in (2, 3, 4, 22, 23, 24):
        return " дня "
    else:
        return " дней "


def hours_string(hours_number: int) -> str:
    """
    :param hours_number: hours quantity
    :return: russian quantity hours string
    """
    if hours_number % 10 == 1 and hours_number != 11:
        return " час "
    elif hours_number in (2, 3, 4, 22, 23):
        return " часа "
    else:
        return " часов "


def minutes_string(minutes_number: int) -> str:
    """

    :param minutes_number: minutes quantity
    :return: russian quantity minutes string
    """
    if minutes_number % 10 == 1 and minutes_number != 11:
        return " минута "
    elif minutes_number not in(12, 13, 14) and minutes_number % 10 in (2, 3, 4):
        return " минуты "
    else:
        return " минут "


if __name__ == "__main__":
    print(seconds_to_russian_string(548344))
    for i in range(1, 31):
        print(seconds_to_russian_string(86900 * i))
