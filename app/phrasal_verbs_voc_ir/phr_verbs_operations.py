from collections import namedtuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from flask import current_app
from enum import Enum, auto
from random import shuffle
from sqlalchemy import exc as sa_exc
from app import db
from app.time_functions import next_quest_time
from app.models import PhrasalVerbsVocabulary, LearnedPhrasalVerbs, IntervalPhrasalVerbs
phr_verb_ir_operation_result = namedtuple("phr_verb_ir_operation_result", "new_verb_voc_inst message")


@dataclass
class VerbAddingResultDC:
    phrasal_verb: str
    translation: str
    is_success: bool


@dataclass
class VerbsFillingResultDC:
    verbs_transl_list: list
    count: int


# from sqlalchemy import exc as fa_exc
# except fa_exc.IntegrityError:
# sqlalchemy.exc.OperationalError: - Mysql connection not available


class MessagesPhrasalVerbsIR(Enum):
    internet_disconnected = auto()
    phrs_verb_available_in_user_voc = auto()
    phrs_verb_not_available_in_user_voc = auto()
    searched_phrs_verb_not_available = auto()
    phrs_verb_was_deleted_successfully = auto()
    phrs_verb_was_added_successfully = auto()
    lost_phrs_verb_progress_was_nullified = auto()
    user_vocabulary_is_empty = auto()
    verbs_were_added_successfully = auto()
    no_more_verbs_to_add = auto()
    lost_verbs_successful_restoring = auto()
    lost_verbs_restoring_exception = auto()
    verbs_vocabulary_was_updated = auto()


flashed_messages_dict_phrs_vrb_ir = {
    MessagesPhrasalVerbsIR.internet_disconnected: "Проверьте подключение к интернету",
    MessagesPhrasalVerbsIR.phrs_verb_available_in_user_voc: "Фразовый глагол {verb} уже есть в Вашем словаре",
    MessagesPhrasalVerbsIR.phrs_verb_not_available_in_user_voc: "Фразового глагола {verb} в словаре нет",
    MessagesPhrasalVerbsIR.searched_phrs_verb_not_available: "Фразового глагола {verb} в словаре нет",
    MessagesPhrasalVerbsIR.phrs_verb_was_deleted_successfully: "Фразовый глагол {verb} был успешно удален из "
                                                               "Вашего словаря",
    MessagesPhrasalVerbsIR.phrs_verb_was_added_successfully: "Фразовый глагол {verb} был успешно добавлен",
    MessagesPhrasalVerbsIR.lost_phrs_verb_progress_was_nullified: "Прогресс изучения выбранных глаголов обнулен",
    MessagesPhrasalVerbsIR.user_vocabulary_is_empty: "Ваш словарь пуст. Добавьте что-нибудь.",
    MessagesPhrasalVerbsIR.verbs_were_added_successfully: "Новые слова были добавлены в Ваш словарь {count}",
    MessagesPhrasalVerbsIR.no_more_verbs_to_add: "Все известные нам фразовые глаголы уже в Вашем словаре",
    MessagesPhrasalVerbsIR.lost_verbs_successful_restoring: "Прогресс изучения пропущенных слов восстановлен",
    MessagesPhrasalVerbsIR.lost_verbs_restoring_exception: "Ошибка восстановления прогресса пропущенных слов",
    MessagesPhrasalVerbsIR.verbs_vocabulary_was_updated: "Словарь фразовых глаголов пополнен {count}",
}


class PhrasalVerbsVocabularyActionsIR:
    def __init__(self, user):
        self.phrasal_verb_text_file = current_app.config.get('PHRASAL_VOCABULARY_PATH')
        self.user = user
        self.repeating_time = None

    @staticmethod
    def search_pattern_creator(verb) -> str:
        """Returns a pattern to proper looking for a words combination in vocabulary
        for example: the pattern for "to prevail" is '%to%prevail%',
        for 'the strongest fear' is '%the%strongest%fear%' and so on
        """
        verb_arr = [f"%{i}" for i in verb.split()]
        res_patt = "".join(verb_arr) + "%"
        return res_patt

    def verb_available_in_voc(self, phrs_verb: str) -> PhrasalVerbsVocabulary or None:
        """Checks for word availability in vocabulary"""
        phrs_verb_pattern = self.search_pattern_creator(phrs_verb)
        return PhrasalVerbsVocabulary.query.filter(PhrasalVerbsVocabulary.key_word.like(phrs_verb_pattern)).first()

    def verb_available_in_user_voc(self, phrs_verb: str = None, verb_voc_inst: PhrasalVerbsVocabulary = None) \
            -> IntervalPhrasalVerbs or None:
        """Checks for word availability in user's vocabulary. Use the generator."""
        phrs_verb_voc_inst = self.verb_available_in_voc(phrs_verb) if phrs_verb else verb_voc_inst
        return IntervalPhrasalVerbs.query.filter_by(user_id=self.user.id,
                                                    word_id=phrs_verb_voc_inst.id).first() if phrs_verb_voc_inst \
            else None

    def verb_addition(self, verb_to_add: str, status=1):
        """Checks for phrasal verb availability in both vocabularies. If verb available
        in general vocabulary, translation is got from general vocabulary.
        In another case messages about verb's availability is flashed
        If word isn't available in user's vocabulary word and it's translation add to
        The function returns namedtuple object includes
            fields: 'new_phrs_verb_voc_inst',
                    'message': MessagesPhrasalVerbsIR - Enum object
                    """
        verb_exists_in_voc = self.verb_available_in_voc(verb_to_add)
        if verb_exists_in_voc:
            """Phrasal verb exists in user vocabulary returns PhrasalVerbsVocabulary instance and success message"""
            user_voc_verb_inst = self.verb_available_in_user_voc(verb_voc_inst=verb_exists_in_voc)
            if user_voc_verb_inst:
                return phr_verb_ir_operation_result(new_verb_voc_inst=verb_exists_in_voc,
                                                    message=MessagesPhrasalVerbsIR.phrs_verb_available_in_user_voc
                                                    )
            else:
                """Adding word to association table"""
                repeating_time = next_quest_time(status)
                words_inst_new_word = IntervalPhrasalVerbs(user=self.user, status=status,
                                                           vocabulary=verb_exists_in_voc,
                                                           repeating_time=repeating_time,
                                                           addition_time=datetime.utcnow(),
                                                           )
                db.session.add(words_inst_new_word)
                db.session.commit()
            return phr_verb_ir_operation_result(new_verb_voc_inst=verb_exists_in_voc,
                                                message=MessagesPhrasalVerbsIR.phrs_verb_was_added_successfully
                                                )
        else:
            """Phrasal verb doesn't exists in vocabulary returns vocabulary instance and unavailable message"""
            return phr_verb_ir_operation_result(None, MessagesPhrasalVerbsIR.phrs_verb_not_available_in_user_voc)

    def delete_word(self, phrs_verb_to_delete: str) -> MessagesPhrasalVerbsIR:
        """Checks for word availability in user vocabulary. If word is available
        in user's vocabulary it deletes it and returns message about successful deleting.
        In another case returns message informed about word absent.
        """
        phrs_verb_to_del_voc_inst = self.verb_available_in_user_voc(phrs_verb_to_delete)
        if not phrs_verb_to_del_voc_inst:
            return MessagesPhrasalVerbsIR.phrs_verb_not_available_in_user_voc
        else:
            with db.session.no_autoflush:
                assoc_inst_phrs_verb_to_delete = IntervalPhrasalVerbs.query. \
                    filter_by(user_id=self.user.id). \
                    filter_by(word_id=phrs_verb_to_del_voc_inst.id). \
                    first()
                db.session.delete(assoc_inst_phrs_verb_to_delete)
                db.session.commit()
            return MessagesPhrasalVerbsIR.phrs_verb_was_deleted_successfully

    def show_user_verbs(self, page_num: int) -> IntervalPhrasalVerbs:
        """Returns pagination object of all words in user vocabulary,
        sorting by the asc. time_to_repeate"""
        user_phrs_verb_voc_pagin_obj = self.user.interval_phrasal_verbs.order_by(IntervalPhrasalVerbs.time_to_repeat). \
            paginate(per_page=10, page=page_num, error_out=True)
        return user_phrs_verb_voc_pagin_obj

    def search_verb_in_user_voc(self, phrasal_verb) -> PhrasalVerbsVocabulary or None:
        """Check if the word is available at user vocabulary.
        If true, returns the Vocabulary object else, return None"""
        phrasal_verbs_vocabulary_inst = self.verb_available_in_user_voc(phrasal_verb)
        return phrasal_verbs_vocabulary_inst.vocabulary if phrasal_verbs_vocabulary_inst else None

    def next_quest_sec_calcul(self):
        """The function calculates  for every word in user's vocabulary
        the difference between the current time and the time that user
        have to repeat word at. The time difference transform to second's count.
        If a TypeError is raised, all the instances, where repeating_time is None are deleted.
        """
        try:
            for iw_inst in self.user.interval_phrasal_verbs.all():
                iw_inst.time_to_repeat = (iw_inst.repeating_time - datetime.now()). \
                    total_seconds()
                db.session.add(iw_inst)
        except TypeError:
            null_repeating_time = IntervalPhrasalVerbs.query. \
                filter(IntervalPhrasalVerbs.repeating_time.is_(None)).all()
            for null_rep_time_inst in null_repeating_time:
                db.session.delete(null_rep_time_inst)
        db.session.commit()

    def test_objects_creating(self):
        """
        Function retrive all the repeating time for each user instance IntervalWords table.
        Than received a vocabulary
        {"lost_test_obj": lost_test,
        "missing_test_obj": missing_test,
        "near_test_obj": near_test}
        The dictionary values are IntervalWords objects
        where
        lost_test_obj - lost test more than one day ago
        missing_test_obj - lost test, but less one day ago
        near_test_obj - test should be complitted for two hours,
            if not it will become lost one
        """
        time_for_losing_test = timedelta(1).total_seconds()
        near_test_time = timedelta(hours=2).total_seconds()
        lost_test_obj = self.user.interval_phrasal_verbs. \
            filter(IntervalPhrasalVerbs.time_to_repeat <= time_for_losing_test.__neg__())
        missing_test_obj = self.user.interval_phrasal_verbs. \
            filter(IntervalPhrasalVerbs.time_to_repeat <= 0). \
            filter(IntervalPhrasalVerbs.time_to_repeat >= time_for_losing_test.__neg__()). \
            order_by(IntervalPhrasalVerbs.time_to_repeat)
        near_test_obj = self.user.interval_phrasal_verbs. \
            filter(IntervalPhrasalVerbs.time_to_repeat <= near_test_time). \
            filter(IntervalPhrasalVerbs.time_to_repeat > 0)
        learned_test_obj = self.user.learned_phrasal_verbs.order_by(LearnedPhrasalVerbs.addition_time.desc())
        return {"lost_test_obj": lost_test_obj, "missing_test_obj": missing_test_obj,
                "near_test_obj": near_test_obj, "learned_test_obj": learned_test_obj}

    def show_near_verbs(self, page_num):
        """Select from table interval_words all the user's words those repeating time
        is less than 2 hours.
        Function returns pagination_object with words per page equal 10.
        """
        near_test_time = timedelta(hours=2).total_seconds()
        near_phrs_verbs_pagin_obj = self.user.interval_phrasal_verbs. \
            filter(IntervalPhrasalVerbs.time_to_repeat <= near_test_time). \
            paginate(per_page=10, page=page_num, error_out=True)
        return near_phrs_verbs_pagin_obj

    def show_missing_verbs(self, page_num):
        """Select from table interval_words all the user's words those repeating time
        is more than -1 day.
        Function returns pagination_object with words per page equal 10.
        """
        time_for_losing_test = timedelta(1).total_seconds()
        missing_test_obj = self.user.interval_phrasal_verbs. \
            filter(IntervalPhrasalVerbs.time_to_repeat <= 0). \
            filter(IntervalPhrasalVerbs.time_to_repeat >= time_for_losing_test.__neg__()). \
            order_by(IntervalPhrasalVerbs.time_to_repeat.desc()). \
            paginate(per_page=10, page=page_num, error_out=True)
        return missing_test_obj

    def show_lost_verbs(self, page_num):
        """Select from table interval_words all the user's words
        that had should been repeated earlier than 1 day ago .
        Function returns pagination_object with words per page equal 10.
        """
        time_for_losing_test = timedelta(1).total_seconds()
        lost_words_pagin_obj = self.user.interval_phrasal_verbs. \
            filter(IntervalPhrasalVerbs.time_to_repeat <= time_for_losing_test.__neg__()). \
            paginate(per_page=10, page=page_num, error_out=True)
        return lost_words_pagin_obj

    def show_learned_verbs(self, page_num):
        """Select from table interval_words all the user's words
        that had should been repeated earlier than 1 day ago .
        Function returns pagination_object with words per page equal 10.
        """
        learned_words_pagin_obj = self.user.learned_phrasal_verbs. \
            paginate(per_page=10, page=page_num, error_out=True)
        return learned_words_pagin_obj

    def drop_down_progress(self, page_num):
        """Select from table interval_words all the user's words
        that had should been repeated earlier than 1 day ago .
        For pagination_object with words per page equal 10 set status to 1
        and repeating_time to now() in interval1
        """
        repeating_time = next_quest_time(1)
        lost_words_pagin_obj = self.show_lost_verbs(page_num)
        for iw_inst in lost_words_pagin_obj.items:
            iw_inst.repeating_time, iw_inst.status = repeating_time, 1
            db.session.add(iw_inst)
        db.session.commit()
        return True

    def phrasal_verbs_list_creating_from_text_file(self):
        with open(self.phrasal_verb_text_file, "r") as file:
            phrasal_verbs_list = [
                [sentence.strip() for sentence in line[1:].split(" = ")]
                for line in file.readlines() if line.startswith("*")
            ]
        return phrasal_verbs_list

    def phrasal_verbs_vocabulary_populating_from_text_file(self):
        phrasal_verbs_list = self.phrasal_verbs_list_creating_from_text_file()
        number = 0
        for verb in phrasal_verbs_list:
            if len(verb) == 5 and not PhrasalVerbsVocabulary.query.filter(
                    PhrasalVerbsVocabulary.phrasal_verb == verb[0],
                    PhrasalVerbsVocabulary.translation == verb[2]
            ).all():
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
                continue
        else:
            return number

    def verb_addition_to_user_verbs_table(self, verb_id_to_add, status=1) -> IntervalPhrasalVerbs or False:
        repeating_time = next_quest_time(status)
        verb_vocabulary_instance = PhrasalVerbsVocabulary.query.get(verb_id_to_add)
        try:
            new_verb_inst = IntervalPhrasalVerbs(user=self.user, status=status,
                                                 vocabulary=verb_vocabulary_instance,
                                                 repeating_time=repeating_time,
                                                 addition_time=datetime.utcnow())
            db.session.add(new_verb_inst)
            db.session.commit()
        except sa_exc:
            db.session.rollback()
            return VerbAddingResultDC(verb_vocabulary_instance.phrasal_verb,
                                      verb_vocabulary_instance.translation, False)

        return VerbAddingResultDC(verb_vocabulary_instance.phrasal_verb,
                                  verb_vocabulary_instance.translation, True)

    def user_verbs_vocabulary_fill(self, count: int = 10):
        successful_added_verbs = 0
        verbs_translations_list = []
        if not self.user:
            return False
        all_verbs = [verb.id for verb in PhrasalVerbsVocabulary.query.all()]
        all_users_verbs = db.session.query(IntervalPhrasalVerbs, PhrasalVerbsVocabulary.id).\
            filter_by(user_id=self.user.id).\
            join(PhrasalVerbsVocabulary, IntervalPhrasalVerbs.word_id == PhrasalVerbsVocabulary.id).all()
        all_users_verbs_id = [verb.id for verb in all_users_verbs]
        verbs_id_to_add = list(set(all_verbs).difference(all_users_verbs_id))
        shuffle(verbs_id_to_add)
        """Verb's ids to add to the user's table"""
        for verb_id in verbs_id_to_add:
            verb_adding_result = self.verb_addition_to_user_verbs_table(verb_id)
            if not verb_adding_result.is_success:
                continue
            successful_added_verbs += 1
            verbs_translations_list.append((verb_adding_result.phrasal_verb, verb_adding_result.translation))
            if successful_added_verbs == count:
                break
        return VerbsFillingResultDC(verbs_translations_list, successful_added_verbs)

    def restore_lost_verbs_handler(self) -> bool:
        """For all of the lost verbs sets repeating_time = datetime.now(),
        returns True in success case or False if sqlalchemy exception was raised."""
        lost_verbs = self.user.interval_phrasal_verbs.filter(IntervalPhrasalVerbs.time_to_repeat < -86400).all()
        for verb in lost_verbs:
            verb.repeating_time = datetime.now()
            db.session.add(verb)
        try:
            db.session.commit()
            return True
        except sa_exc:
            db.session.rollback()
            return False


"""next_quest_sec_calcul description
        Порядок действий:
        <st> time_diff = iw_inst.repeating_time - datetime.now() --> timedelta(days=int, seconds=int)
        <st> total_seconds = timediff.total_seconds() - Количtство секунд. Заносится в базу данных
            = time_to_repeat
        <st> В зависимости от знака и количества секунд разделение на группы:
            1) Отрицательное количество секунд:
                1.1 По модулю больше 86400 - цикл повторения будет начат заново
                filter(IntervalWords.time_to_repeat <= -86400)
                    -- lost_test_days, lost_test_time = str(timedelta(seconds=total_seconds)).split(" days, ")
                    -- lost_test_hours, lost_test_minutes = lost_test_time.split(":")[1:]
                1.2 По модулю менее 86400 - Пропущенные тесты
                filter(IntervalWords.time_to_repeat <= 0,
                IntervalWords.time_to_repeat >= -86400)
                    -- missing_test_hours, missing_test_minutes = str(timedelta(seconds=total_seconds)).split(":")[1:]

            2) Положительное количество секунд:
                 2.1 кол-во секунд < 7200 но больше 0, текущий тест
                filter(IntervalWords.time_to_repeat Ю 0,
                IntervalWords.time_to_repeat >= 7200)
                    -- near_test_days, near_test_time = str(timedelta(seconds=total_seconds)).split(" days, ")
                    -- near_test_hours, near_test_minutes = near_test_time.split(":")[1:]

        <st> days_time_tpl = str(timedelta(seconds=total_seconds)).split(" days, ")
            Время в часах, минутах, секундах
        <st> days_quantity = int(total_sec_str.split("days")[0]) ("23455")
        <st> time_ = total_sec_str.split("days")[1] ("12:12:12")
        <st> hours, minutes = time_.split(":")[1:]"""


# def seconds_to_days_time(seconds: int) -> dict:
#     """Receive seconds quantity and return number of days, hours, and minutes"""
#     total_days, time_ = str(timedelta(seconds=seconds)).split(" days, ") \
#         if seconds >= 86400 else ("", str(timedelta(seconds=seconds)))
#     months = int(total_days) // 30 \
#         if total_days and int(total_days) > 29 else 0
#     days = int(total_days) % 30 if months else total_days
#     hours, minutes = time_.split(":")[:2]
#     return {"months": months, "days": days, "hours": hours, "minutes": minutes}


if __name__ == "__main__":
    pass
