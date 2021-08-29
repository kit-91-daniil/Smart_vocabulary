from flask import Blueprint, render_template, request, redirect, url_for, \
    flash, session
from flask_security import current_user, login_required
from app.ir_voc.forms import WordAddInputForm, WordDeleteInputForm, SearchWordForm
from app.ir_voc.vocabulary_operations_ir import VocabularyActionsIR, MessagesIR, \
    flashed_messages_dict_ir
from app.time_transform import seconds_to_russian_string

ir_voc = Blueprint("ir_voc", __name__,
                   template_folder="templates",
                   static_folder="static"
                   )


@ir_voc.route("/")
@login_required
def user_voc():
    add_word_form = WordAddInputForm(word=session.get("new_word_ir", ""))
    delete_word_form = WordDeleteInputForm(request.form)
    vocabulary_actions_ir = VocabularyActionsIR(current_user)
    vocabulary_actions_ir.next_quest_sec_calcul()
    words_status_dict = vocabulary_actions_ir.test_objects_creating()
    # assert isinstance(words_status_dict, dict), ["The result object has wrong type. Not dict"]
    result = render_template("ir_voc/translator_ir.html",
                             add_word_form=add_word_form,
                             delete_word_form=delete_word_form,
                             words_status_dict=words_status_dict,
                             type=type, seconds_to_string=seconds_to_russian_string,
                             )
    session["translating_result_ir"] = None
    session["new_word_ir"] = None
    return result


@ir_voc.route("/add_word", methods=["POST", "GET"])
@login_required
def add_word():
    add_word_form = WordAddInputForm(request.form)
    delete_word_form = WordDeleteInputForm(request.form)
    word_to_translate = add_word_form.word.data
    if request.method == 'POST' and add_word_form.validate():
        vocabulary_actions = VocabularyActionsIR(current_user)
        translating_result_voc_obj = vocabulary_actions.new_word(word_to_translate)
        message = translating_result_voc_obj.message
        if message == MessagesIR.word_was_added_successfully:
            session["translating_result_ir"] = translating_result_voc_obj.new_word_voc_inst.translation
            session["new_word_ir"] = word_to_translate
            message_string = flashed_messages_dict_ir[MessagesIR.word_was_added_successfully].\
                format(word=word_to_translate)
            flash(message_string, category="info")
        elif message == MessagesIR.internet_disconnected:
            message_string = flashed_messages_dict_ir[message]
            flash(message_string, category="danger")
        else:
            message_string = flashed_messages_dict_ir[message].format(word=word_to_translate)
            flash(message_string, category="info")
        return redirect(url_for("ir_voc.user_voc"))
    else:
        vocabulary_actions_ir = VocabularyActionsIR(current_user)
        vocabulary_actions_ir.next_quest_sec_calcul()
        words_status_dict = vocabulary_actions_ir.test_objects_creating()
        # assert isinstance(words_status_dict, dict), ["The result object has wrong type. Not dict"]
        result = render_template("ir_voc/translator_ir.html",
                                 add_word_form=add_word_form,
                                 delete_word_form=delete_word_form,
                                 words_status_dict=words_status_dict,
                                 type=type, seconds_to_string=seconds_to_russian_string,
                                 )
        session["translating_result_ir"] = None
        session["new_word_ir"] = None
        return result


@ir_voc.route("/delete_word", methods=["POST", "GET"])
@login_required
def delete_word():
    add_word_form = WordAddInputForm(request.form)
    delete_word_form = WordDeleteInputForm(request.form)
    if request.method == 'POST' and delete_word_form.validate():
        word_to_delete = delete_word_form.word.data
        vocabulary_actions = VocabularyActionsIR(current_user)
        deleting_word_result = vocabulary_actions.delete_word(word_to_delete)
        if deleting_word_result == MessagesIR.word_not_available_in_user_voc:
            deleting_message = flashed_messages_dict_ir[MessagesIR.word_not_available_in_user_voc]
            flash(message=deleting_message, category="info")
        elif deleting_word_result == MessagesIR.word_was_deleted_successfully:
            deleting_message = flashed_messages_dict_ir[MessagesIR.word_was_deleted_successfully].\
                format(word=word_to_delete)
            flash(deleting_message, category="info")
        return redirect(url_for("ir_voc.user_voc"))
    else:
        vocabulary_actions_ir = VocabularyActionsIR(current_user)
        vocabulary_actions_ir.next_quest_sec_calcul()
        words_status_dict = vocabulary_actions_ir.test_objects_creating()
        # assert isinstance(words_status_dict, dict), ["The result object has wrong type. Not dict"]
        result = render_template("ir_voc/translator_ir.html",
                                 add_word_form=add_word_form,
                                 delete_word_form=delete_word_form,
                                 words_status_dict=words_status_dict,
                                 type=type, seconds_to_string=seconds_to_russian_string,
                                 )
        session["translating_result_ir"] = None
        session["new_word_ir"] = None
        return result


@ir_voc.route("/show_user_voc_ir/<int:page_num>/<int:translation_available>",
              methods=["POST", "GET"])
@login_required
def show_user_voc_ir(page_num, translation_available):
    word_to_search_form = SearchWordForm(word=session.get("searching_word_ir", ""))
    vocabulary_actions_ir = VocabularyActionsIR(current_user)
    user_words_ir_pagin_obj_ir = vocabulary_actions_ir.show_user_words(page_num)
    result = render_template("ir_voc/user_vocabulary_ir.html",
                             user_words_pagin_obj_ir=user_words_ir_pagin_obj_ir,
                             word_to_search_form=word_to_search_form,
                             translation_available=translation_available,
                             abs=abs, seconds_to_string=seconds_to_russian_string,
                             )
    session["searching_word_ir"] = ""
    session["searching_word_translation_ir"] = ""
    return result


@ir_voc.route("/search_user_word/<int:page_num>/<int:translation_available>", methods=["GET", "POST"])
@login_required
def search_word_user_voc(page_num, translation_available):
    word_to_search_form = SearchWordForm(request.form)
    word_to_search = word_to_search_form.word.data
    if request.method == "POST" and word_to_search_form.validate():
        vocabulary_actions_ir = VocabularyActionsIR(current_user)
        searching_result = vocabulary_actions_ir.check_user_voc_for_word_availability(word_to_search)
        if searching_result:
            session["searching_word_ir"] = searching_result.word
            session["searching_word_translation_ir"] = searching_result.translation
        else:
            search_message = flashed_messages_dict_ir[MessagesIR.searching_word_not_available]
            flash(search_message, category="info")
    return redirect(url_for("ir_voc.show_user_voc_ir", page_num=page_num,
                            translation_available=translation_available))


@ir_voc.route("/near_words/<int:page_num>/<int:translation_available>",
              methods=["POST", "GET"])
@login_required
def show_near_words(page_num=1, translation_available=0):
    vocabulary_actions_ir = VocabularyActionsIR(current_user)
    near_words_pagin_obj = vocabulary_actions_ir.show_near_words(page_num)
    result = render_template("ir_voc/words_to_repeat.html",
                             near_words_pagin_obj=near_words_pagin_obj,
                             translation_available=translation_available,
                             abs=abs, seconds_to_string=seconds_to_russian_string,
                             )
    return result


@ir_voc.route("/missing_words/<int:page_num>/<int:translation_available>",
              methods=["POST", "GET"])
@login_required
def show_missing_words(page_num=1, translation_available=0):
    vocabulary_actions_ir = VocabularyActionsIR(current_user)
    missing_words_pagin_obj = vocabulary_actions_ir.show_missing_words(page_num)
    result = render_template("ir_voc/words_to_repeat.html",
                             missing_words_pagin_obj=missing_words_pagin_obj,
                             translation_available=translation_available, abs=abs,
                             seconds_to_string=seconds_to_russian_string,
                             )
    return result


@ir_voc.route("/lost_words/<int:page_num>/<int:translation_available>",
              methods=["POST", "GET"])
@login_required
def show_lost_words(page_num=1, translation_available=0):
    vocabulary_actions_ir = VocabularyActionsIR(current_user)
    lost_words_pagin_obj = vocabulary_actions_ir.show_lost_words(page_num)
    result = render_template("ir_voc/words_to_repeat.html",
                             lost_words_pagin_obj=lost_words_pagin_obj,
                             translation_available=translation_available,
                             abs=abs, seconds_to_string=seconds_to_russian_string,
                             )
    return result


@ir_voc.route("/learned_words/<int:page_num>/<int:translation_available>",
              methods=["POST", "GET"])
@login_required
def show_learned_words(page_num=1, translation_available=0):
    vocabulary_actions_ir = VocabularyActionsIR(current_user)
    learned_words_pagin_obj = vocabulary_actions_ir.show_learned_words(page_num)
    result = render_template("ir_voc/words_to_repeat.html",
                             learned_words_pagin_obj=learned_words_pagin_obj,
                             translation_available=translation_available,
                             abs=abs, seconds_to_string=seconds_to_russian_string,
                             )
    return result


@ir_voc.route("/drop_down_progress/<int:page_num>", methods=["POST", "GET"])
@login_required
def drop_down_progress(page_num):
    vocabulary_actions_ir = VocabularyActionsIR(current_user)
    vocabulary_actions_ir.drop_down_progress(page_num)
    message_string = flashed_messages_dict_ir[MessagesIR.lost_word_progress_was_nullified]
    flash(message_string, category="info")
    return redirect(url_for("ir_voc.user_voc", page_num=1,
                            translation_available=0))


@ir_voc.route("/add_random_words", methods=["GET"])
@login_required
def add_random_words():
    vocabulary_actions_ir = VocabularyActionsIR(current_user)
    user_vocabulary_filling_result = vocabulary_actions_ir.user_vocabulary_fill()
    message_string = flashed_messages_dict_ir[
        MessagesIR.words_were_added_successfully].format(count=user_vocabulary_filling_result.count) \
        if isinstance(user_vocabulary_filling_result.count, int) \
        else flashed_messages_dict_ir[MessagesIR.words_adding_error]

    flash(message=message_string, category="info")
    return redirect(url_for("ir_voc.user_voc"))


@ir_voc.route("/update_vocabulary", methods=["GET"])
@login_required
def update_vocabulary():
    vocabulary_actions_ir = VocabularyActionsIR(current_user)
    vocabulary_actions_ir.update_vocabulary()
    flash("Words were successfully added", category="info")
    return redirect(url_for("ir_voc.user_voc"))


@ir_voc.route("/restore_lost_words", methods=["GET"])
@login_required
def restore_lost_words():
    vocabulary_actions_ir = VocabularyActionsIR(current_user)
    restoring_result = vocabulary_actions_ir.restore_lost_words_handler()
    message = flashed_messages_dict_ir[MessagesIR.lost_words_successful_restoring] \
        if restoring_result else flashed_messages_dict_ir[MessagesIR.lost_words_restoring_exception]
    flash(message=message, category="info")
    return redirect(url_for("ir_voc.user_voc"))


if __name__ == "__main__":
    pass
