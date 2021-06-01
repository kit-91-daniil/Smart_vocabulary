import os
from app.models import *
from sqlalchemy import exc
cd = os.getcwd()
os.path.abspath(os.curdir)
os.chdir("../preparing_for_EPAM_exam/english_lexic")
english_words_path = os.path.join(os.getcwd(), "english_words")


def integrity_error_handling():
    try:
        new_voc_inst = Vocabulary(word="branch", translation="ответвление")
        db.session.add(new_voc_inst)
        db.session.commit()
    except exc.IntegrityError:
        print("smth wrong")
        db.session.rollback()


if __name__ == "__main__":
    with open(english_words_path, "r") as e_words_file:
        for j, i in enumerate(e_words_file.readlines(), 1):
            print(j, i, end="")
