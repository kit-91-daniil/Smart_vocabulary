from datetime import timedelta, datetime

intervals = {
    1: timedelta(hours=4),
    2: timedelta(1),
    3: timedelta(3),
    4: timedelta(7),
    5: timedelta(15),
    6: timedelta(30),
    7: timedelta(60),
    "time_for_losing_test": timedelta(1).total_seconds(),

}


def seconds_to_next_quest(status):
    return int(timedelta.total_seconds(intervals[status]))


def next_quest_time(status: int) -> datetime:
    """
    :param status:
    :return:
    Принимает статус и на основании статуса и текущего времени вычисляет время следующего опроса"""
    return datetime.now() + intervals[status]


if __name__ == "__main__":
    print(next_quest_time(1))
    print(datetime.utcnow())
