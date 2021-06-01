from collections import namedtuple
from datetime import datetime, timedelta
from enum import Enum, auto
from app import db
from app.translation import translate_word, TranslatorMessages
from app.time_functions import next_quest_time
from app.models import Vocabulary, IntervalWords, LearnedWords

new_word_add_ir = namedtuple("new_word_add_nt", "new_word_voc_inst message")

# from sqlalchemy import exc as fa_exc
# except fa_exc.IntegrityError:
# sqlalchemy.exc.OperationalError: - Mysql connection not available


class MessagesIR(Enum):
    internet_disconnected = auto()
    word_available_in_user_voc = auto()
    word_not_available_in_user_voc = auto()
    searching_word_not_available = auto()
    word_was_deleted_succesfully = auto()
    word_was_added_succesfully = auto()
    word_can_not_been_translated = auto()
    lost_word_progress_was_nullified = auto()


flashed_messages_dict_ir = {
    MessagesIR.internet_disconnected: "Проверьте подключение к интернету",
    MessagesIR.word_available_in_user_voc: "Слово {word} уже есть в Вашем словаре",
    MessagesIR.word_not_available_in_user_voc: "Такого слова в словаре нет",
    MessagesIR.searching_word_not_available: "Такого слова в словаре нет",
    MessagesIR.word_was_deleted_succesfully: "Слово {word} было успешно удалено",
    MessagesIR.word_was_added_succesfully: "Слово {word} было успешно добавлено",
    MessagesIR.word_can_not_been_translated: "Слово {word} не может быть переведено",
    MessagesIR.lost_word_progress_was_nullified: "Прогресс изучения выбранных слов обнулен"
}


class VocabularyActionsIR:
    def __init__(self, user):
        self.user = user
        self.repeating_time = None

    @staticmethod
    def check_voc_for_word_availability(word):
        """Checks for word availability in vocabulary"""
        return Vocabulary.query.filter(Vocabulary.word == word).first()

    def check_user_voc_for_word_availability(self, word: str) -> object or False:
        """Checks for word availability in user's vocabulary. Use the generator."""
        user_voc_words = (i.vocabulary.word for i in self.user.interval_words.all())
        user_voc_inst_word = Vocabulary.query.filter(Vocabulary.word == word).first()
        return user_voc_inst_word if word in user_voc_words else None

    def new_word(self, word_to_add: str, status=1):
        """Checks for word availability in both vocabularies. If word available
        in general vocabulary, translation get from general vocabulary.
        In another case translation received from translator.
        If word isn't available in user's vocabulary word and it's translation add to
        user's table.
        The function returns namedtuple object with
            fields: 'new_word_voc_inst',
                    'message': MessagesIR - Enum object
                    """
        word_exist_in_voc = self.check_voc_for_word_availability(word_to_add)
        repeating_time = next_quest_time(status)
        if word_exist_in_voc:
            """Word exist in vocabulary"""
            user_voc_word_inst = self.check_user_voc_for_word_availability(word_to_add)
            voc_inst_new_word = Vocabulary.query.filter(Vocabulary.word == word_to_add).first()
            if user_voc_word_inst:
                return new_word_add_ir(new_word_voc_inst=voc_inst_new_word,
                                       message=MessagesIR.word_available_in_user_voc
                                       )
            else:
                """Adding word to association table"""
                words_inst_new_word = IntervalWords(user=self.user, status=status,
                                                    vocabulary=voc_inst_new_word,
                                                    repeating_time=repeating_time,
                                                    addition_time=datetime.utcnow(),
                                                    )
                db.session.add(words_inst_new_word)
                db.session.commit()
            return new_word_add_ir(new_word_voc_inst=voc_inst_new_word,
                                   message=MessagesIR.word_was_added_succesfully
                                   )
        else:
            """Need to translator by the translator"""
            translator_output_nt = translate_word(word_to_add)
            translator_output_message = translator_output_nt.message
            if translator_output_message == TranslatorMessages.success:
                translator_output_word = translator_output_nt.translation
                voc_inst_new_word = Vocabulary(word=word_to_add,
                                               translation=translator_output_word,
                                               )
                words_inst_new_word = IntervalWords(user=self.user, status=status,
                                                    vocabulary=voc_inst_new_word,
                                                    repeating_time=repeating_time,
                                                    addition_time=datetime.utcnow(),
                                                    )
                db.session.add_all([voc_inst_new_word, words_inst_new_word])
                db.session.commit()
                return new_word_add_ir(voc_inst_new_word, MessagesIR.word_was_added_succesfully)
            elif translator_output_message == TranslatorMessages.can_not_been_translated:
                """Incorrect symbols or Too long result"""
                return new_word_add_ir(None, MessagesIR.word_can_not_been_translated)
            else:
                return new_word_add_ir(None, MessagesIR.internet_disconnected)

    def delete_word(self, word_to_delete):
        """Checks for word availability in user vocabulary. If word is available
        in user's vocabulary it deletes and returns message about successful deleting.
        In another case returns message informed about word absent.
        """
        word_to_del_voc_inst = self.check_user_voc_for_word_availability(word_to_delete)

        if not word_to_del_voc_inst:
            return MessagesIR.word_not_available_in_user_voc
        else:
            with db.session.no_autoflush:
                assoc_inst_word_to_delete = IntervalWords.query. \
                    filter_by(user_id=self.user.id). \
                    filter_by(word_id=word_to_del_voc_inst.id). \
                    first()
                db.session.delete(assoc_inst_word_to_delete)
                db.session.commit()
            return MessagesIR.word_was_deleted_succesfully

    def show_user_words(self, page_num):
        """Returns pagination object of all words in user vocabulary,
        sorting by the asc. time_to_repeate"""
        user_voc_pagin_obj = self.user.interval_words.order_by(IntervalWords.time_to_repeat). \
            paginate(per_page=10, page=page_num, error_out=True)
        return user_voc_pagin_obj

    def search_word_in_user_voc(self, word):
        """Check if the word is available at user vocabulary.
        If true, returns the Vocabulary object else, return None"""
        return self.check_user_voc_for_word_availability(word)

    def next_quest_sec_calcul(self):
        """The function calculates  for every word in user's vocabulary
        the difference between the current time and the time that user
        have to repeat word at. The time difference transform to second's quantity.
        If TypeError was raised, all the instances define, where repeating_time is None.
        Function deletes all these instances.
        """
        try:
            for iw_inst in self.user.interval_words.all():
                iw_inst.time_to_repeat = (iw_inst.repeating_time - datetime.now()). \
                    total_seconds()
                db.session.add(iw_inst)
        except TypeError:
            null_repeating_time = IntervalWords.query. \
                filter(IntervalWords.repeating_time.is_(None)).all()
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
        lost_test_obj = self.user.interval_words. \
            filter(IntervalWords.time_to_repeat <= time_for_losing_test.__neg__())
        missing_test_obj = self.user.interval_words. \
            filter(IntervalWords.time_to_repeat <= 0). \
            filter(IntervalWords.time_to_repeat >= time_for_losing_test.__neg__()). \
            order_by(IntervalWords.time_to_repeat.desc())
        near_test_obj = self.user.interval_words. \
            filter(IntervalWords.time_to_repeat <= near_test_time). \
            filter(IntervalWords.time_to_repeat > 0)
        learned_test_obj = self.user.learned_words.order_by(LearnedWords.addition_time.desc())
        return {"lost_test_obj": lost_test_obj, "missing_test_obj": missing_test_obj,
                "near_test_obj": near_test_obj, "learned_test_obj": learned_test_obj}

    def show_near_words(self, page_num):
        """Select from table interval_words all the user's words those repeating time
        is less than 2 hours.
        Function returns pagination_object with words per page equal 10.
        """
        near_test_time = timedelta(hours=2).total_seconds()
        near_words_pagin_obj = self.user.interval_words. \
            filter(IntervalWords.time_to_repeat <= near_test_time). \
            paginate(per_page=10, page=page_num, error_out=True)
        return near_words_pagin_obj

    def show_missing_words(self, page_num):
        """Select from table interval_words all the user's words those repeating time
        is more than -1 day.
        Function returns pagination_object with words per page equal 10.
        """
        time_for_losing_test = timedelta(1).total_seconds()
        missing_test_obj = self.user.interval_words. \
            filter(IntervalWords.time_to_repeat <= 0). \
            filter(IntervalWords.time_to_repeat >= time_for_losing_test.__neg__()). \
            order_by(IntervalWords.time_to_repeat.desc()). \
            paginate(per_page=10, page=page_num, error_out=True)
        return missing_test_obj

    def show_lost_words(self, page_num):
        """Select from table interval_words all the user's words
        that had should been repeated earlier than 1 day ago .
        Function returns pagination_object with words per page equal 10.
        """
        time_for_losing_test = timedelta(1).total_seconds()
        lost_words_pagin_obj = self.user.interval_words. \
            filter(IntervalWords.time_to_repeat <= time_for_losing_test.__neg__()). \
            paginate(per_page=10, page=page_num, error_out=True)
        return lost_words_pagin_obj

    def show_learned_words(self, page_num):
        """Select from table interval_words all the user's words
        that had should been repeated earlier than 1 day ago .
        Function returns pagination_object with words per page equal 10.
        """
        learned_words_pagin_obj = self.user.learned_words. \
            paginate(per_page=10, page=page_num, error_out=True)
        return learned_words_pagin_obj

    def drop_down_progress(self, page_num):
        """Select from table interval_words all the user's words
        that had should been repeated earlier than 1 day ago .
        For pagination_object with words per page equal 10 set status to 1
        and repeating_time to now() in interval1
        """
        repeating_time = next_quest_time(1)
        lost_words_pagin_obj = self.show_lost_words(page_num)
        for iw_inst in lost_words_pagin_obj.items:
            iw_inst.repeating_time, iw_inst.status = repeating_time, 1
            db.session.add(iw_inst)
        db.session.commit()
        return True


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


def seconds_to_days_time(seconds: int) -> dict:
    """Receive seconds quantity and return number of days, hours, and minutes"""
    total_days, time_ = str(timedelta(seconds=seconds)).split(" days, ") \
        if seconds >= 86400 else ("", str(timedelta(seconds=seconds)))
    months = int(total_days) // 30 \
        if total_days and int(total_days) > 29 else 0
    days = int(total_days) % 30 if months else total_days
    hours, minutes = time_.split(":")[:2]
    return {"months": months, "days": days, "hours": hours, "minutes": minutes}


if __name__ == "__main__":
    pass
