from datetime import timedelta
from itertools import combinations
from app import create_app
from app.models import *
from app.time_functions import next_quest_time
from datetime import datetime


def timedelta_creator(hour):
    return datetime.now() + timedelta(hours=hour)


hours_list = [1, 3, 8, 6, 7, 9, 12]
td_list = list(map(timedelta_creator, hours_list))
td_list.insert(3, None)
td_list.insert(4, 4)


# for i in td_list:
#     print(i)


def appender(lst):
    res_lst = []
    try:
        for j in lst:
            res_lst.append(j - datetime.now())
    except TypeError:
        for u in list(filter(lambda f: not isinstance(f, datetime), lst)):
            lst.remove(u)
        return appender(lst)
    return res_lst


# for x in appender(td_list):
#     print(x)


def homogenous_arr(arr):
    res_lst = []
    for ins_arr in arr:
        if ins_arr and len(set([type(v) for v in ins_arr])) == 1:
            res_lst.append(ins_arr)
    return res_lst


arr1 = [[1, 2, 3, 4], ["a", 2, "b"], [], ["a", "b", "c"]]


def every_possible_sum(number):
    arr_str = combinations(str(number), 2)
    return [int(i) + int(j) for (i, j) in arr_str]


# print(every_possible_sum(1234))


app = create_app()
app_ctx = app.app_context()
app_ctx.push()


def adding_words(limit, offset):
    all_words = Vocabulary.query.offset(offset).limit(limit).all()
    user1 = User.query.first()
    repeating_time = next_quest_time(1)
    for i in all_words:
        iw_inst = IntervalWords(user=user1, status=1, vocabulary=i,
                                repeating_time=repeating_time,
                                addition_time=datetime.utcnow()
                                )
        db.session.add(iw_inst)
    db.session.commit()
    return "words were succesfully added"


def cleaning_the_vocabulary(user_id):
    iw_a = IntervalWords.query.filter_by(user_id=user_id).all()
    word_list = [i.word_id for i in iw_a]
    print(word_list)
    print(len(word_list))
    print(len(set(word_list)))


# print(adding_words(20, 80))
# cleaning_the_vocabulary(1)

def summmm(a, b):
    return a + b

# print(summmm(3,4))
