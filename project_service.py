import os
from enum import Enum, auto
from sqlalchemy import exc
from app import create_app
from app.models import Vocabulary, User, db
from app.ir_voc.vocabulary_operations_ir import VocabularyActionsIR as va_ir


class ActionsResults(Enum):
    success = auto()
    integrity_error = auto()


cd = os.getcwd()
os.path.abspath(os.curdir)
os.chdir("../preparing_for_EPAM_exam/english_lexic")
english_words_path = os.path.join(os.getcwd(), "english_words")


def vocabulary_fill(text_file_path) -> ActionsResults:
    """Receives a word_translation arr and add every words with
    it's translation to the vocabulary. In case of duplicating word
    will not be added"""
    app = create_app()
    app_ctx = app.app_context()
    app_ctx.push()
    words_transl_arr = word_transl_gen_creator_from_file(text_file_path)
    for w_tr_tpl in words_transl_arr:
        try:
            new_voc_inst = Vocabulary(word=w_tr_tpl[0], translation=w_tr_tpl[1])
            db.session.add(new_voc_inst)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            print(ActionsResults.integrity_error, w_tr_tpl)
        except IndexError:
            db.session.rollback()
            print(f"Index Error. Word {w_tr_tpl} have noted incorrect")
    return ActionsResults.success


def word_transl_gen_creator_from_file(file_path):
    """the file must have the following pattern:
    word - translation;
    """
    with open(file_path) as text_file:
        res_str = text_file.read()
    res_gen = [pair.split(" - ") for pair in res_str.split(";\n")]
    return res_gen


def user_voc_fill_from_text_file(email: str, text_file_path: str,
                                 count: int = 10, offset: int = 0):
    with open(text_file_path) as text_file:
        res_str = text_file.read()
    word_list = [pair.split("-")[0] for pair in res_str.split(";\n")]
    app = create_app()
    app_ctx = app.app_context()
    app_ctx.push()
    user = User.query.filter(User.email == email).first()
    va_ir_inst = va_ir(user)
    words_adding_messages = []
    for word in word_list[offset:offset + count]:
        try:
            word_adding_result = va_ir_inst.new_word(word).message
            words_adding_messages.append(word_adding_result)
        except exc.IntegrityError:
            db.session.rollback()
    print(words_adding_messages)

    # adding_result = [va_ir_inst.new_word(word).message for word in word_list[offset:offset + count]]
    # print(adding_result)


os.chdir("/home/dan/home/programming/preparing_for_EPAM_exam/english_lexic")
phrase_verbs_path = os.path.join(os.getcwd(), "phrase_verbs")
phrase_verbs_changed_path = os.path.join(os.getcwd(), "phrase_verbs_changed")


def phrase_verbs_changing(file, file_changed):
    with open(file, "r") as file_context:
        changing_strings = [
            i.replace("	", "= ") for i in file_context.readlines() if "	" in i
        ]
    with open(file_changed, "w") as new_file:
        new_file.writelines(changing_strings)


if __name__ == "__main__":
    # vocabulary_fill(english_words_path)
    user_voc_fill_from_text_file("dan2@mail.ru", english_words_path, 81, 10)
    # pass
    # phrase_verbs_changing(phrase_verbs_path, phrase_verbs_changed_path)
