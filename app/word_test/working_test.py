from datetime import timedelta
from flask import session
import difflib
from sqlalchemy import func
from app.models import Vocabulary, Words, IntervalWords, LearnedWords
from app import db
from app.time_functions import next_quest_time

"""sqlalchemy.exc.InvalidRequestError"""


def similarily(s1, s2):
    matcher = difflib.SequenceMatcher(None, s1.lower(), s2.lower())
    return matcher.ratio()


def check_answer(answer_to_check, word_number, sim=0.8):
    right_answer = session["words_translations_test"][word_number][1]
    return "right" \
        if similarily(answer_to_check, right_answer) > sim \
        else "wrong"


class TestChecker:
    def __init__(self, user):
        self.user = user
        self.time_for_losing_test = timedelta(1).total_seconds()
        self.near_test_time = timedelta(hours=2).total_seconds()
        self.words_quantity = 10

    flash_messages_test = {
    }

    def word_status_increment(self, word_id):
        iw_inst = self.user.interval_words.\
            filter(IntervalWords.word_id == word_id).first()
        if iw_inst.status == 7:
            db.session.delete(iw_inst)
            l_w_voc_inst = Vocabulary.query.get(word_id)
            learned_words_inst = LearnedWords(user=self.user, vocabulary=l_w_voc_inst)
            db.session.add(learned_words_inst)
            db.session.commit()
            return l_w_voc_inst
        iw_inst.status += 1
        iw_inst.repeating_time = next_quest_time(iw_inst.status)
        db.session.add(iw_inst)
        db.session.commit()

    def base_query_object_random_words_creating(self):
        """Returns the BaseQuery object with random words and their translations.
         BaseQuery objects consist values (Vocabulary.word, Vocabulary.translation)"""
        return db.session. \
            query(Words, Vocabulary.word, Vocabulary.translation, Vocabulary.id). \
            filter_by(user_id=self.user.id).order_by(func.random())

    def base_query_object_random_interval_words_creating(self):
        """Returns the BaseQuery object with random words, learned by
        interval repeating system and their translations.
         BaseQuery objects consist values (Vocabulary.word, Vocabulary.translation)"""
        return db.session. \
            query(IntervalWords, Vocabulary.word, Vocabulary.translation, Vocabulary.id). \
            filter_by(user_id=self.user.id).order_by(func.random())

    def base_query_object_near_words_creating(self):
        """Returns the BaseQuery object with words that's time_to_repeat_value is
        from 0 and to near_test_time (2 hours by default).
        BaseQuery objects consist values Vocabulary.word, Vocabulary.translation"""
        return db.session. \
            query(IntervalWords, Vocabulary.word, Vocabulary.translation, Vocabulary.id). \
            filter_by(user_id=self.user.id). \
            filter(IntervalWords.time_to_repeat <= self.near_test_time). \
            filter(IntervalWords.time_to_repeat > 0)

    def base_query_object_missing_words_creating(self):
        """Returns the BaseQuery object with words that's time_to_repeat_value is
        from time_for_losing_test (1 day by default) and 0.
        BaseQuery object consist values (Vocabulary.word, Vocabulary.translation)"""
        return db.session. \
            query(IntervalWords, Vocabulary.word, Vocabulary.translation, Vocabulary.id). \
            filter_by(user_id=self.user.id). \
            filter(IntervalWords.time_to_repeat <= 0). \
            filter(IntervalWords.time_to_repeat >= self.time_for_losing_test.__neg__())

    def base_query_object_lost_words_creating(self):
        """Returns the BaseQuery object with words that's time_to_repeat_value is
        less than time_for_losing_test (1 day by default)
        BaseQuery object consist values (Vocabulary.word, Vocabulary.translation)"""
        return db.session. \
            query(IntervalWords, Vocabulary.word, Vocabulary.translation, Vocabulary.id). \
            filter_by(user_id=self.user.id). \
            filter(IntervalWords.time_to_repeat <= self.time_for_losing_test.__neg__())

    def base_query_object_learned_words_creating(self):
        """Returns the BaseQuery object LearnedWords table. It consist already learned words.
        BaseQuery object consist values (Vocabulary.word, Vocabulary.translation)"""
        return db.session. \
            query(LearnedWords, Vocabulary.word, Vocabulary.translation, Vocabulary.id). \
            filter_by(user_id=self.user.id)

    def create_the_word_list_for_test(self, base_query_object):
        """Receives BaseQuery object and returns list of tuples
        (Vocabulary.word, Vocabulary.translation) limited by words_quantity value"""
        base_query_words_for_test = base_query_object. \
            join(Vocabulary, Words.word_id == Vocabulary.id). \
            order_by(func.random()).limit(self.words_quantity)
        words_translations_for_test = \
            [(voc.word, voc.translation)
             for voc in base_query_words_for_test.all()]
        return words_translations_for_test

    def create_the_interval_word_list_for_test(self, base_query_object):
        """Receives BaseQuery object and returns list of tuples
        (Vocabulary.word, Vocabulary.translation) limited by words_quantity value"""
        base_query_words_for_test = base_query_object. \
            join(Vocabulary, IntervalWords.word_id == Vocabulary.id). \
            order_by(func.random()).limit(self.words_quantity)
        words_translations_for_test = \
            [(voc.word, voc.translation, voc.id)
             for voc in base_query_words_for_test.all()]
        return words_translations_for_test

    def create_the_learned_word_list_for_test(self, base_query_object):
        """Receives BaseQuery object and returns list of tuples
        (Vocabulary.word, Vocabulary.translation) limited by words_quantity value"""
        base_query_words_for_test = base_query_object. \
            join(Vocabulary, LearnedWords.word_id == Vocabulary.id). \
            order_by(func.random()).limit(self.words_quantity)
        words_translations_for_test = \
            [(voc.word, voc.translation, voc.id)
             for voc in base_query_words_for_test.all()]
        return words_translations_for_test

    def test_object_creating(self, test_type: str):
        """Function creates """
        if test_type == "random":
            return self.create_the_word_list_for_test(
                self.base_query_object_random_words_creating()
            )
        elif test_type == "random_interval":
            return self.create_the_interval_word_list_for_test(
                self.base_query_object_random_interval_words_creating()
            )
        elif test_type == "near":
            return self.create_the_interval_word_list_for_test(
                self.base_query_object_near_words_creating()
            )
        elif test_type == "missing":
            return self.create_the_interval_word_list_for_test(
                self.base_query_object_missing_words_creating()
            )
        elif test_type == "lost":
            return self.create_the_interval_word_list_for_test(
                self.base_query_object_lost_words_creating()
            )
        elif test_type == "learned":
            return self.create_the_learned_word_list_for_test(
                self.base_query_object_learned_words_creating()
            )
