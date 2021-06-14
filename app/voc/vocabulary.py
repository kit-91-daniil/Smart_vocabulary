from flask import Blueprint, render_template, request, redirect, url_for, \
    flash, session
from flask_security import current_user, login_required
from app.voc.forms import WordAddInputForm, WordDeleteInputForm, SearchWordForm
from app.voc.vocabulary_operations import VocabularyActions, Messages, flashed_messages_dict
voc = Blueprint("voc", __name__, template_folder="templates", static_folder="static")


@voc.route("/")
@login_required
def user_voc():
    add_word_form = WordAddInputForm(word=session.get("new_word", ""))
    delete_word_form = WordDeleteInputForm(request.form)
    result = render_template("voc/translator.html",
                             add_word_form=add_word_form,
                             delete_word_form=delete_word_form
                             )
    session["translating_result"] = None
    return result


@voc.route("/add_word", methods=["GET", "POST"])
@login_required
def add_word():
    add_word_form = WordAddInputForm(request.form)
    delete_word_form = WordDeleteInputForm(request.form)
    word_to_translate = add_word_form.word.data
    if request.method == 'POST' and add_word_form.validate():
        vocabulary_actions = VocabularyActions(current_user)
        translating_result_voc_obj = vocabulary_actions.new_word(word_to_translate)
        message = translating_result_voc_obj.message
        if message == Messages.word_was_added_successfully:
            session["translating_result"] = translating_result_voc_obj.new_word_voc_inst.translation
            session["new_word"] = word_to_translate
            message_string = flashed_messages_dict[Messages.word_was_added_successfully].\
                format(word=word_to_translate)
            flash(message_string, category="info")
        elif message == Messages.internet_disconnected:
            message_string = flashed_messages_dict[message]
            flash(message_string, category="danger")
        else:
            message_string = flashed_messages_dict[message].format(word=word_to_translate)
            flash(message_string, category="info")
        return redirect(url_for("voc.user_voc"))
    else:
        return render_template("voc/translator.html",
                               add_word_form=add_word_form,
                               delete_word_form=delete_word_form
                               )


@voc.route("/Delete_word", methods=["GET", "Post"])
@login_required
def delete_word():
    add_word_form = WordAddInputForm(request.form)
    delete_word_form = WordDeleteInputForm(request.form)
    if request.method == 'POST' and delete_word_form.validate():
        word_to_delete = delete_word_form.word.data
        vocabulary_actions = VocabularyActions(current_user)
        deleting_word_result = vocabulary_actions.delete_word(word_to_delete)
        if deleting_word_result == Messages.word_not_available_in_user_voc:
            deleting_message = flashed_messages_dict[Messages.word_not_available_in_user_voc]
            flash(message=deleting_message, category="info")
        elif deleting_word_result == Messages.word_was_deleted_successfully:
            deleting_message = flashed_messages_dict[Messages.word_was_deleted_successfully].\
                format(word=word_to_delete)
            flash(deleting_message, category="info")
        return redirect(url_for("voc.user_voc"))
    else:
        return render_template("voc/translator.html",
                               add_word_form=add_word_form,
                               delete_word_form=delete_word_form
                               )


@voc.route("/user_voc/<int:page_num>", methods=["GET"])
@login_required
def show_user_voc(page_num=1):
    word_to_search = SearchWordForm(word=session.get("searching_word", ""))
    vocabulary_actions = VocabularyActions(current_user)
    user_words_pagin_obj = vocabulary_actions.show_user_words(page_num)
    result = render_template("voc/user_vocabulary.html",
                             user_words_pagin_obj=user_words_pagin_obj,
                             word_to_search=word_to_search, dir=dir
                             )
    session["searching_word"] = ""
    session["searching_word_translation"] = ""
    return result


@voc.route("/search_user_word/<int:page_num>", methods=["GET", "POST"])
@login_required
def search_word_user_voc(page_num):
    word_to_search_form = SearchWordForm(request.form)
    word_to_search = word_to_search_form.word.data
    if request.method == "POST" and word_to_search_form.validate():
        vocabulary_actions = VocabularyActions(current_user)
        searching_result = vocabulary_actions.check_user_voc_for_word_availability(word_to_search)
        if searching_result:
            session["searching_word"] = searching_result.word
            session["searching_word_translation"] = searching_result.translation
            result = redirect(url_for("voc.show_user_voc", page_num=page_num))
            return result
        else:
            flash(flashed_messages_dict[Messages.searching_word_not_available],
                  category="info")
            return redirect(url_for("voc.show_user_voc", page_num=page_num))
    return redirect(url_for("voc.show_user_voc", page_num=page_num))


if __name__ == "__main__":
    pass
