# FEATURES
"""hasattr"""
# if hasattr(fields. "items"):
#     fields = fields.items()

# if hasattr(self, "items"):
#     fields = self.items()


dct1 = {
    "a": 12,
    "b": 13,
    "c": 14,
}


def summa(a, b, c):
    return 2 * a + 1 * b + 1 * c


# print(summa(**dct1))


def sum1(*args):
    for i in args:
        print(i)


def multiplicate(a):
    return 2 * a


class Number:
    def __init__(self, a, b):
        self.a = multiplicate(a)
        self.b = b

    def __repr__(self):
        return f"{self.a=}, {self.b=}"


dct1 = {"a": "aaa",
        "b": "bbb",
        "c": "ccc", }


# dct1["a"] = "zzz"
# print(dct1["a"])

class LoginForm:
    def __init__(self, x=14):
        self.x = x

    var = dct1.get("a", "")


class CustomLoginForm(LoginForm):
    def __init__(self):
        super(CustomLoginForm, self).__init__()

    dct1["a"] = "yyy"
    var = dct1.get("a", "")


# lf = LoginForm()
# print(lf.var)
# clf = CustomLoginForm()
# print(clf.var)

def func1(x):
    return "func1" + x


# print(func1.__call__(" rrr"))
# print(func1.__call__("rrr"))

"""
# Beginning Python backend developer seeking for improve skills as junior python developer
#     
# - Experience with Python.
# - Some experience in designing and development of web service based on Flask-Python.
# - Basic understanding of front-end technologies, such as HTML5, CSS3 and UI development experience (Bootstrap4).
# - Database knowledge and python interaction with databases (MySQL) familiarity with ORM (Object Relational Mapper) libraries (SQLAlchemy).
# - Good experience in python object oriented programming.
# - Has no experience in commercial development.

Communicative, open-minded beginner Python seeks for join a developers team as junior python backend developer. Eager to lear, conscientious, motivated and enthusiastic about career change and development skills goal. 
"""
'''
1 1
1 2
2 3
3 5
5 8
8 13
13 21
'''
unknown_words = ["treat", "prevent", "common", "unintentionally",
                 "valid", "occur", "aliase", "enforce", "explicit", ""]


def fib(n):
    """Функция вычисления числа Фиббоначи"""
    a = b = 1
    for i in range(n - 2):
        a, b = b, a + b
    return b


# print(fib(7))
from abc import abstractmethod, ABC


class BaseClass(ABC):
    @abstractmethod
    def say_hi(self):
        print("Hi")


class Cls1(BaseClass):
    def say_hi(self):
        print("hi from cls1")


class Cls2(BaseClass):
    def say_hi(self):
        super(Cls2, self).say_hi()
        print("hi from cls2")


#
# c1 = Cls1()
# c2 = Cls2()
# c1.say_hi()
# c2.say_hi()
"""
Добавление слова 
в виртуальный словарь с интервальными повторениями
 1. Проверить есть ли это слово в общем словаре
  - если оно есть, вернуть. Если нет - перевести
 2. вычислить время повторения repeating_time
 sec_to_time
"""
import os

file_dir = "D:\programming\python\MYSQL_CONSPECT"
file_name = "datetime_routine.html"
file_name1 = "sandy.html"
filename = os.path.join(file_dir, file_name)
filename1 = os.path.join(file_dir, file_name1)
# print(filename)


def html_file_redactor(filename_: str):
    with open(filename_) as f1, open(filename_, "a") as ft:
        for line in f1.readlines():
            if "<" not in line and not line.isspace():
                new_line = line.split("()")
                ft.write(
                    f'<tr>'
                    f'<td class="table_name">{new_line[0]}</td>'
                    f'<td class="table_description">{new_line[1]}</td>'
                    f'</tr>')
                ft.write("\n")


# html_file_redactor(filename1)


def html_file_redactor1(filename_: str):
    with open(filename_) as f1, open(filename_, "a") as ft:
        for line in f1.readlines():
            print(line)
            # if "<" not in line and not line.isspace():
            #     new_line = line.split("()")
            #     ft.write(
            #         f'<tr>'
            #         f'<td class="table_name">{new_line[0]}</td>'
            #         f'<td class="table_description">{new_line[1]}</td>'
            #         f'</tr>')
            #     ft.write("\n")


# html_file_redactor1(filename)


def decor(func):
    cache = {}

    def wrapper(x):
        if x in cache:
            print("cache")
            return cache[x]
        else:
            res = func(x)
            cache[x] = res
            return res

    return wrapper

@decor
def double(x):
    return x * 2


def terminal_working():
    from app import create_app
    app = create_app()
    app_ctx = app.app_context()
    app_ctx.push()
    return app

"""Устанавливает время в секундах до следующего опроса.
        Порядок действий:
        <st> time_diff = iw_inst.repeating_time - datetime.now() --> timedelta(days=int, seconds=int)
        <st> total_seconds = timediff.total_seconds() - Количtство секунд. Заносится в базу данных
            = time_to_repeat
        <st> В зависимости от знака и количества секунд разделение на группы:
            1) Отрицательное количество секунд:
                1.1 По модулю больше 86400 - цикл повторения будет начат заново
                filter(IntervalWords.time_to_repeat <= 86400 )
                    -- lost_test_days, lost_test_time = str(timedelta(seconds=total_seconds)).split(" days, ")
                    -- lost_test_hours, lost_test_minutes = lost_test_time.split(":")[1:]
                1.2 По модулю менее 86400 - Пропущенные тесты
                filter(IntervalWords.time_to_repeat <= 0,
                IntervalWords.time_to_repeat >= -86400)
                    -- missing_test_hours, missing_test_minutes = str(timedelta(seconds=total_seconds)).split(":")[1:]

            2) Положительное количество секунд:
                 2.1 кол-во секунд < 7200 но больше 0, текущий тест
                filter(IntervalWords.time_to_repeat > 0,
                IntervalWords.time_to_repeat < 7200)
                    -- near_test_days, near_test_time = str(timedelta(seconds=total_seconds)).split(" days, ")
                    -- near_test_hours, near_test_minutes = near_test_time.split(":")[1:]

        <st> days_time_tpl = str(timedelta(seconds=total_seconds)).split(" days, ")
            Время в часах, минутах, секундах
        <st> days_quantity = int(total_sec_str.split("days")[0]) ("23455")
        <st> time_ = total_sec_str.split("days")[1] ("12:12:12")
        <st> hours, minutes = time_.split(":")[1:]

        """