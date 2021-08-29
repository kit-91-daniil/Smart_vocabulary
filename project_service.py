import os
from enum import Enum, auto
from sqlalchemy import exc as sa_exc
from datetime import datetime
from random import shuffle
from app import create_app
from app.models import Vocabulary, User, db, IntervalWords, \
    PhrasalVerbsVocabulary, IntervalPhrasalVerbs
from app.ir_voc.vocabulary_operations_ir import VocabularyActionsIR as VocabularyActionsIr
from app.time_functions import next_quest_time
from config import phrasal_vocabulary_path, vocabulary_path


class ActionsResults(Enum):
    success = auto()
    integrity_error = auto()


# cd = os.getcwd()
# os.path.abspath(os.curdir)
# os.chdir("../preparing_for_EPAM_exam/english_lexic")
# english_words_path = os.path.join(os.getcwd(), "english_words")
# os.chdir("/home/dan/home/programming/preparing_for_EPAM_exam/english_lexic")
# phrasal_verbs_path = os.path.join(os.getcwd(), "phrase_verbs")
# phrasal_verbs_changed_path = os.path.join(os.getcwd(), "phrase_verbs_changed")
# phrasal_verbs_new_file = os.path.join(os.getcwd(), "phrasal_verbs_refactored")


def app_context_manager(func):
    def wrapper(*args, **kwargs):
        app = create_app()
        app_ctx = app.app_context()
        app_ctx.push()
        return func(*args, **kwargs)
    return wrapper


def left_strip(text_file_path):
    with open(text_file_path) as text_before:
        lines = [line.lstrip() for line in text_before.readlines() if line.__len__() > 4]
    with open(text_file_path, "a") as text_after:
        text_after.writelines(lines)


def word_translation_list_creator_from_file(file_path):
    """the file must have the following pattern:
    word - translation;
    """
    with open(file_path) as text_file:
        word_translation_list = [[sentence.strip() for sentence in line[1:].split(" - ")]
                                 for line in text_file.readlines() if line.startswith("*")]
    return word_translation_list


def update_vocabulary(text_file_path) -> ActionsResults:
    """Receives a word_translation arr and add every words with
    it's translation to the vocabulary. In case of duplicating word
    will not be added"""
    words_transl_list = word_translation_list_creator_from_file(text_file_path)
    for w_tr_tpl in words_transl_list:
        try:
            new_voc_inst = Vocabulary(word=w_tr_tpl[0], translation=w_tr_tpl[1])
            db.session.add(new_voc_inst)
            db.session.commit()
        except sa_exc.IntegrityError or IndexError:
            db.session.rollback()
    return ActionsResults.success


@app_context_manager
def allowing_lost_words():
    """For every of the lost words defines repeating_time equal datetime.now()"""
    u1 = User.query.first()
    lost_words = u1.interval_words.filter(IntervalWords.time_to_repeat < 0).all()
    for word in lost_words:
        word.repeating_time = datetime.now()
        db.session.add(word)
    try:
        db.session.commit()
        print("Lost words were successfully repaired")
        return True
    except sa_exc.DatabaseError:
        db.session.rollback()


@app_context_manager
def user_voc_fill_from_text_file(email: str, text_file_path: str,
                                 count: int = 10, offset: int = 0):
    with open(text_file_path) as text_file:
        res_str = text_file.read()
    word_list = [pair.split("-")[0] for pair in res_str.split(";\n")]
    user = User.query.filter(User.email == email).first()
    va_ir_inst = VocabularyActionsIr(user)
    words_adding_messages = []
    for word in word_list[offset:offset + count]:
        try:
            word_adding_result = va_ir_inst.new_word(word).message
            words_adding_messages.append(word_adding_result)
        except sa_exc.IntegrityError:
            db.session.rollback()
    print(words_adding_messages)


def phrasal_verbs_refactoring(file, new_file):
    """Refactors phrasal verbs text file by doubling phrasal_verb
    for therefore makes from it phrasal verb key word"""
    app = create_app()
    app_ctx = app.app_context()
    app_ctx.push()
    with open(file, "r") as file_original:
        original_file_lines_list = [sentence for sentence in file_original.readlines()]
    new_file_content = []
    for line in original_file_lines_list:
        line_consist = line.split("=") if len(line) > 1 else ""
        if isinstance(line_consist, list):
            line_consist.insert(0, line_consist[0])
            result_line = "= ".join(line_consist)
            print(result_line)
        else:
            result_line = ""
        new_file_content.append(result_line)
    with open(new_file, "w") as new_file:
        new_file.writelines(new_file_content)


def phrasal_verbs_list_creating_from_text_file(phrasal_verb_file):
    with open(phrasal_verb_file, "r") as file:
        phrasal_verbs_list = [
            [sentence.strip() for sentence in line[1:].split(" = ")]
            for line in file.readlines() if line.startswith("*")
        ]
    return phrasal_verbs_list


@app_context_manager
def phrasal_verbs_vocabulary_populating_from_text_file(phrasal_verbs_text_file):
    phrasal_verbs_list = phrasal_verbs_list_creating_from_text_file(phrasal_verbs_text_file)
    app = create_app()
    app_ctx = app.app_context()
    app_ctx.push()
    number = 0
    for verb in phrasal_verbs_list:
        if len(verb) == 5:
            phrasal_verb_vocabulary_inst = PhrasalVerbsVocabulary(
                phrasal_verb=verb[0], key_word=verb[1], translation=verb[2],
                description=verb[3], example=verb[4],
            )
            try:
                db.session.add(phrasal_verb_vocabulary_inst)
                db.session.commit()
                number += 1
            except sa_exc.IntegrityError:
                db.session.rollback()
                continue
        else:
            print(f"Phrasal Verb {verb} is not correctly written down")
            continue
    else:
        print(f"{number} Words were added")


def verb_addition_to_user_verbs_table(user, verb_id_to_add, status=1) -> IntervalPhrasalVerbs or False:
    repeating_time = next_quest_time(status)
    verb_vocabulary_instance = PhrasalVerbsVocabulary.query.get(verb_id_to_add)
    try:
        new_verb_inst = IntervalPhrasalVerbs(user=user, status=status,
                                             vocabulary=verb_vocabulary_instance,
                                             repeating_time=repeating_time,
                                             addition_time=datetime.utcnow())
        db.session.add(new_verb_inst)
        db.session.commit()
    except sa_exc:
        db.session.rollback()
        return verb_vocabulary_instance
    return False


@app_context_manager
def user_phrasal_vocabulary_populate(user_email: str, count: int):
    successful_added_verbs = 0
    cur_user = User.query.filter(User.email == user_email).first()
    if not cur_user:
        return False
    all_verbs = [verb.id for verb in PhrasalVerbsVocabulary.query.all()]
    all_users_verbs = db.session.query(IntervalPhrasalVerbs, PhrasalVerbsVocabulary.id).\
        filter_by(user_id=cur_user.id).\
        join(PhrasalVerbsVocabulary, IntervalPhrasalVerbs.word_id == PhrasalVerbsVocabulary.id).all()
    all_users_verbs_id = [verb.id for verb in all_users_verbs]
    verbs_id_to_add = list(set(all_verbs).difference(all_users_verbs_id))
    shuffle(verbs_id_to_add)
    """Verb's ids to add to the user's table"""
    for verb_id in verbs_id_to_add:
        if verb_addition_to_user_verbs_table(cur_user, verb_id):
            continue
        successful_added_verbs += 1
        if successful_added_verbs == count:
            break
    return successful_added_verbs


if __name__ == "__main__":
    left_strip(vocabulary_path)
