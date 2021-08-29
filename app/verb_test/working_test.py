from datetime import timedelta
from flask import session
import difflib
from sqlalchemy import func
from app.models import PhrasalVerbs, IntervalPhrasalVerbs, LearnedPhrasalVerbs, PhrasalVerbsVocabulary
from app import db
from app.time_functions import next_quest_time

"""sqlalchemy.exc.InvalidRequestError"""


def similarity(s1, s2):
    matcher = difflib.SequenceMatcher(None, s1.lower(), s2.lower())
    return matcher.ratio()


def check_answer(answer_to_check, right_answer, sim=0.8):
    return "right" \
        if similarity(answer_to_check, right_answer) > sim \
        else "wrong"


class VerbsTestCreator:
    def __init__(self, user):
        self.user = user
        self.time_for_losing_test = timedelta(1).total_seconds()
        self.near_test_time = timedelta(hours=2).total_seconds()
        self.words_count = 10

    def verb_status_increment(self, verb_id):
        iw_inst = self.user.interval_phrasal_verbs.\
            filter(IntervalPhrasalVerbs.word_id == verb_id).first()
        if not iw_inst:
            return False
        if iw_inst.status == 7:
            db.session.delete(iw_inst)
            learned_verb_voc_inst = PhrasalVerbsVocabulary.query.get(verb_id)
            learned_verbs_inst = LearnedPhrasalVerbs(user=self.user, vocabulary=learned_verb_voc_inst)
            db.session.add(learned_verbs_inst)
            db.session.commit()
            return learned_verb_voc_inst
        iw_inst.status += 1
        iw_inst.repeating_time = next_quest_time(iw_inst.status)
        db.session.add(iw_inst)
        db.session.commit()
        return True

    def base_query_object_random_verbs_creating(self):
        """Returns the BaseQuery object with random words and their translations.
         BaseQuery objects consist values (Vocabulary.word, Vocabulary.translation)"""
        return db.session. \
            query(PhrasalVerbs,
                  PhrasalVerbsVocabulary.phrasal_verb, PhrasalVerbsVocabulary.translation,
                  PhrasalVerbsVocabulary.key_word, PhrasalVerbsVocabulary.description,
                  PhrasalVerbsVocabulary.example, PhrasalVerbsVocabulary.id). \
            filter_by(user_id=self.user.id).order_by(func.random())

    def base_query_object_random_interval_verbs_creating(self):
        """Returns the BaseQuery object with random words, learned by
        interval repeating system and their translations.
         BaseQuery objects consist values (Vocabulary.word, Vocabulary.translation)"""
        return db.session. \
            query(IntervalPhrasalVerbs,
                  PhrasalVerbsVocabulary.phrasal_verb, PhrasalVerbsVocabulary.translation,
                  PhrasalVerbsVocabulary.key_word, PhrasalVerbsVocabulary.description,
                  PhrasalVerbsVocabulary.example, PhrasalVerbsVocabulary.id). \
            filter_by(user_id=self.user.id).order_by(func.random())

    def base_query_object_near_verbs_creating(self):
        """Returns the BaseQuery object with words that's time_to_repeat_value is
        from 0 and to near_test_time (2 hours by default).
        BaseQuery objects consist values Vocabulary.word, Vocabulary.translation"""
        return db.session. \
            query(IntervalPhrasalVerbs,
                  PhrasalVerbsVocabulary.phrasal_verb, PhrasalVerbsVocabulary.translation,
                  PhrasalVerbsVocabulary.key_word, PhrasalVerbsVocabulary.description,
                  PhrasalVerbsVocabulary.example, PhrasalVerbsVocabulary.id). \
            filter_by(user_id=self.user.id). \
            filter(IntervalPhrasalVerbs.time_to_repeat <= self.near_test_time). \
            filter(IntervalPhrasalVerbs.time_to_repeat > 0)

    def base_query_object_missing_verbs_creating(self):
        """Returns the BaseQuery object with words that's time_to_repeat_value is
        from time_for_losing_test (1 day by default) and 0.
        BaseQuery object consist values (Vocabulary.word, Vocabulary.translation)"""
        return db.session. \
            query(IntervalPhrasalVerbs,
                  PhrasalVerbsVocabulary.phrasal_verb, PhrasalVerbsVocabulary.translation,
                  PhrasalVerbsVocabulary.key_word, PhrasalVerbsVocabulary.description,
                  PhrasalVerbsVocabulary.example, PhrasalVerbsVocabulary.id). \
            filter_by(user_id=self.user.id). \
            filter(IntervalPhrasalVerbs.time_to_repeat <= 0). \
            filter(IntervalPhrasalVerbs.time_to_repeat >= self.time_for_losing_test.__neg__())

    def base_query_object_lost_verbs_creating(self):
        """Returns the BaseQuery object with words that's time_to_repeat_value is
        less than time_for_losing_test (1 day by default)
        BaseQuery object consist values (Vocabulary.word, Vocabulary.translation)"""
        return db.session. \
            query(IntervalPhrasalVerbs,
                  PhrasalVerbsVocabulary.phrasal_verb, PhrasalVerbsVocabulary.translation,
                  PhrasalVerbsVocabulary.key_word, PhrasalVerbsVocabulary.description,
                  PhrasalVerbsVocabulary.example, PhrasalVerbsVocabulary.id). \
            filter_by(user_id=self.user.id). \
            filter(IntervalPhrasalVerbs.time_to_repeat <= self.time_for_losing_test.__neg__())

    def base_query_object_learned_verbs_creating(self):
        """Returns the BaseQuery object LearnedWords table. It consist already learned words.
        BaseQuery object consist values (Vocabulary.word, Vocabulary.translation)"""
        return db.session. \
            query(LearnedPhrasalVerbs,
                  PhrasalVerbsVocabulary.phrasal_verb, PhrasalVerbsVocabulary.translation,
                  PhrasalVerbsVocabulary.key_word, PhrasalVerbsVocabulary.description,
                  PhrasalVerbsVocabulary.example, PhrasalVerbsVocabulary.id). \
            filter_by(user_id=self.user.id)

    def create_the_verbs_list_for_test(self, base_query_object):
        """Receives BaseQuery object and returns list of tuples
        (Vocabulary.word, Vocabulary.translation) limited by words_count value"""
        base_query_words_for_test = base_query_object. \
            join(PhrasalVerbsVocabulary, PhrasalVerbs.word_id == PhrasalVerbsVocabulary.id). \
            order_by(func.random()).limit(self.words_count)
        verbs_translations_for_test = \
            [(voc.phrasal_verb, voc.translation, voc.key_word, voc.description, voc.example, voc.id)
             for voc in base_query_words_for_test.all()]
        return verbs_translations_for_test

    def create_the_interval_word_list_for_test(self, base_query_object):
        """Receives BaseQuery object and returns list of tuples
        (Vocabulary.word, Vocabulary.translation) limited by words_count value"""
        base_query_words_for_test = base_query_object. \
            join(PhrasalVerbsVocabulary, IntervalPhrasalVerbs.word_id == PhrasalVerbsVocabulary.id). \
            order_by(func.random()).limit(self.words_count)
        verbs_translations_for_test = \
            [(voc.phrasal_verb, voc.translation, voc.key_word, voc.description, voc.example, voc.id)
             for voc in base_query_words_for_test.all()]
        return verbs_translations_for_test

    def create_the_learned_word_list_for_test(self, base_query_object):
        """Receives BaseQuery object and returns list of tuples
        (Vocabulary.word, Vocabulary.translation) limited by words_count value"""
        base_query_words_for_test = base_query_object. \
            join(PhrasalVerbsVocabulary, LearnedPhrasalVerbs.word_id == PhrasalVerbsVocabulary.id). \
            order_by(func.random()).limit(self.words_count)
        verbs_translations_for_test = \
            [(voc.phrasal_verb, voc.translation, voc.key_word, voc.description, voc.example, voc.id)
             for voc in base_query_words_for_test.all()]
        return verbs_translations_for_test

    def test_object_creating(self, test_type: str):
        """Function creates """
        if test_type == "random_verbs":
            return self.create_the_verbs_list_for_test(
                self.base_query_object_random_verbs_creating()
            )
        elif test_type == "random_interval_verbs":
            return self.create_the_interval_word_list_for_test(
                self.base_query_object_random_interval_verbs_creating()
            )
        elif test_type == "near_verbs":
            return self.create_the_interval_word_list_for_test(
                self.base_query_object_near_verbs_creating()
            )
        elif test_type == "missing_verbs":
            return self.create_the_interval_word_list_for_test(
                self.base_query_object_missing_verbs_creating()
            )
        elif test_type == "lost_verbs":
            return self.create_the_interval_word_list_for_test(
                self.base_query_object_lost_verbs_creating()
            )
        elif test_type == "learned_verbs":
            return self.create_the_learned_word_list_for_test(
                self.base_query_object_learned_verbs_creating()
            )
