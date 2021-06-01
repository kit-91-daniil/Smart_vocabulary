from app.models import Vocabulary, Words
from app import db
from app.translation import translate_word, TranslatorMessages
from collections import namedtuple
from enum import Enum, auto

new_word_add = namedtuple("new_word_add_nt", "new_word_voc_inst message")

# from sqlalchemy import exc as fa_exc
# except fa_exc.IntegrityError:
# sqlalchemy.exc.OperationalError: - Mysql connection not available


class Messages(Enum):
    internet_disconnected = auto()
    word_available_in_user_voc = auto()
    word_not_available_in_user_voc = auto()
    searching_word_not_available = auto()
    word_was_deleted_succesfully = auto()
    word_was_added_succesfully = auto()
    word_can_not_been_translated = auto()


flashed_messages_dict = {
    Messages.internet_disconnected: "Проверьте подключение к интернету",
    Messages.word_available_in_user_voc: "Слово {word} уже есть в Вашем словаре",
    Messages.word_not_available_in_user_voc: "Такого слова в словаре нет",
    Messages.searching_word_not_available: "Такого слова в словаре нет",
    Messages.word_was_deleted_succesfully: "Слово {word} было успешно удалено",
    Messages.word_was_added_succesfully: "Слово {word} было успешно добавлено",
    Messages.word_can_not_been_translated: "Слово {word} не может быть переведено"
}


class VocabularyActions:
    def __init__(self, user):
        self.user = user
        self.alert = None

    @staticmethod
    def check_voc_for_word_availability(word):
        """Checks for word availability in vocabulary"""
        return Vocabulary.query.filter(Vocabulary.word == word).first()

    def check_user_voc_for_word_availability(self, word: str):
        """Checks for word availability in user's vocabulary"""
        user_voc_words = (i.vocabulary.word for i in self.user.words.all())
        user_voc_inst_word = Vocabulary.query.filter(Vocabulary.word == word).first()
        return user_voc_inst_word if word in user_voc_words else None

    def new_word(self, word_to_add: str) -> new_word_add:
        """Checks for word availability in both vocabularies. If word available
        in general vocabulary, translation get from general vocabulary.
        In another case translation received from translator.
        If word isn't available in user's vocabulary word and it's translation add to
        user's table.
        The function returns namedtuple object with
            fields: 'new_word_voc_inst',
                    'message': Messages - Enum object
                    """
        word_exist_in_voc = self.check_voc_for_word_availability(word_to_add)
        if word_exist_in_voc:
            """Word exist in vocabulary"""
            if self.check_user_voc_for_word_availability(word_to_add):
                voc_inst_new_word = Vocabulary.query.filter(Vocabulary.word == word_to_add).first()
                return new_word_add(voc_inst_new_word, Messages.word_available_in_user_voc)
            else:
                """Adding word to association table"""
                voc_inst_word = Vocabulary.query.filter(Vocabulary.word == word_to_add).first()
                words_inst_new_word = Words(user=self.user, vocabulary=voc_inst_word)
                db.session.add(words_inst_new_word)
                db.session.commit()
                return new_word_add(voc_inst_word, Messages.word_was_added_succesfully)
        else:
            """Need to translate by the translator"""
            translator_output_nt = translate_word(word_to_add)
            translator_output_message = translator_output_nt.message
            if translator_output_message == TranslatorMessages.success:
                translator_output_word = translator_output_nt.translation
                voc_inst_new_word = Vocabulary(word=word_to_add,
                                               translation=translator_output_word
                                               )
                words_inst_new_word = Words(user=self.user, vocabulary=voc_inst_new_word)
                db.session.add_all([voc_inst_new_word, words_inst_new_word])
                db.session.commit()
                return new_word_add(voc_inst_new_word, Messages.word_was_added_succesfully)
            elif translator_output_message == TranslatorMessages.can_not_been_translated:
                """Incorrect symbols or Too long result"""
                return new_word_add(None, Messages.word_can_not_been_translated)
            else:
                return new_word_add(None, Messages.internet_disconnected)

    def delete_word(self, word_to_delete) -> Messages:
        """Checks for word availability in user vocabulary. If word is available
        in user's vocabulary it deletes and returns message about successful deleting.
        In another case returns message informed about word absent.
        """
        word_to_del_voc_inst = self.check_user_voc_for_word_availability(word_to_delete)
        if not word_to_del_voc_inst:
            return Messages.word_not_available_in_user_voc
        else:
            with db.session.no_autoflush:
                assoc_inst_word_to_delete = Words.query. \
                    filter_by(user_id=self.user.id). \
                    filter_by(word_id=word_to_del_voc_inst.id). \
                    first()
                db.session.delete(assoc_inst_word_to_delete)
                db.session.commit()
            return Messages.word_was_deleted_succesfully

    def show_user_words(self, page_num):
        user_voc_pagin_obj = self.user.words.order_by(db.desc(Words.addition_time)). \
            paginate(per_page=10, page=page_num, error_out=True)
        return user_voc_pagin_obj

    def search_word_in_user_voc(self, word):
        search_word_result = self.check_user_voc_for_word_availability(word)
        return search_word_result
