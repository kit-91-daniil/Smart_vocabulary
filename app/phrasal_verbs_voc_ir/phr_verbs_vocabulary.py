from flask import Blueprint, render_template, request, redirect, url_for, \
    flash, session
from flask_security import current_user, login_required

from app.phrasal_verbs_voc_ir.forms import PhrasalVerbAddInputForm, PhrasalVerbDeleteInputForm, \
    SearchPhrasalVerbForm

from app.phrasal_verbs_voc_ir.phr_verbs_operations import PhrasalVerbsVocabularyActionsIR, \
    MessagesPhrasalVerbsIR, flashed_messages_dict_phrs_vrb_ir
from app.time_transform import seconds_to_russian_string

phrasal_verbs_voc_ir = Blueprint("phrasal_verbs_voc_ir", __name__,
                                 template_folder="templates",
                                 static_folder="static"
                                 )


@phrasal_verbs_voc_ir.route("/")
@login_required
def user_voc():
    add_phrasal_verb_form = PhrasalVerbAddInputForm(word=session.get("new_verb_ir", ""))
    delete_phrasal_verb_form = PhrasalVerbDeleteInputForm(request.form)
    phrasal_verbs_vocabulary_actions_ir = PhrasalVerbsVocabularyActionsIR(current_user)
    # For all the phrasal verbs are consisted in user's vocabulary calculate time to repeating
    phrasal_verbs_vocabulary_actions_ir.next_quest_sec_calcul()
    words_status_dict = phrasal_verbs_vocabulary_actions_ir.test_objects_creating()
    result = render_template("phrasal_verbs_voc_ir/phrasal_verbs_translator_ir.html",
                             add_phrasal_verb_form=add_phrasal_verb_form,
                             delete_phrasal_verb_form=delete_phrasal_verb_form,
                             words_status_dict=words_status_dict,
                             seconds_to_string=seconds_to_russian_string,
                             )
    session["verb_translation_ir"] = None
    session["new_verb_ir"] = None
    return result


@phrasal_verbs_voc_ir.route("/add_word", methods=["POST", "GET"])
@login_required
def add_word():
    add_verb_form = PhrasalVerbAddInputForm(request.form)
    delete_verb_form = PhrasalVerbDeleteInputForm(request.form)
    verb_to_translate = add_verb_form.phrasal_verb.data
    if request.method == 'POST' and add_verb_form.validate():
        verb_vocabulary_actions = PhrasalVerbsVocabularyActionsIR(current_user)
        verb_addition_result = verb_vocabulary_actions.verb_addition(verb_to_translate)
        message = verb_addition_result.message
        if message == MessagesPhrasalVerbsIR.phrs_verb_was_added_successfully:
            session["verb_translation_ir"] = verb_addition_result.new_verb_voc_inst.translation
            session["new_verb_ir"] = verb_to_translate
            message_string = flashed_messages_dict_phrs_vrb_ir[MessagesPhrasalVerbsIR.phrs_verb_was_added_successfully] \
                .format(verb=verb_to_translate)
            flash(message_string, category="info")
        else:
            message_string = flashed_messages_dict_phrs_vrb_ir[message].format(verb=verb_to_translate)
            flash(message_string, category="info")
        return redirect(url_for("ir_voc.user_voc"))
    else:
        verb_vocabulary_actions = PhrasalVerbsVocabularyActionsIR(current_user)
        verb_vocabulary_actions.next_quest_sec_calcul()
        words_status_dict = verb_vocabulary_actions.test_objects_creating()
        result = render_template("ir_voc/phrasal_verbs_translator_ir.html",
                                 add_word_form=add_verb_form,
                                 delete_word_form=delete_verb_form,
                                 words_status_dict=words_status_dict,
                                 type=type, seconds_to_string=seconds_to_russian_string,
                                 )
        session["verb_translation_ir"] = None
        session["new_verb_ir"] = None
        return result


@phrasal_verbs_voc_ir.route("/delete_word", methods=["POST", "GET"])
@login_required
def delete_word():
    add_verb_form = PhrasalVerbAddInputForm(request.form)
    delete_verb_form = PhrasalVerbDeleteInputForm(request.form)
    verb_vocabulary_actions = PhrasalVerbsVocabularyActionsIR(current_user)
    if request.method == 'POST' and delete_verb_form.validate():
        verb_to_delete = delete_verb_form.phrasal_verb.data
        deleting_verb_result = verb_vocabulary_actions.delete_word(verb_to_delete)
        if deleting_verb_result == MessagesPhrasalVerbsIR.phrs_verb_not_available_in_user_voc:
            deleting_message = flashed_messages_dict_phrs_vrb_ir[
                MessagesPhrasalVerbsIR.phrs_verb_not_available_in_user_voc].format(verb=verb_to_delete)
            flash(message=deleting_message, category="info")
        elif deleting_verb_result == MessagesPhrasalVerbsIR.phrs_verb_was_deleted_successfully:
            deleting_message = flashed_messages_dict_phrs_vrb_ir[
                MessagesPhrasalVerbsIR.word_was_deleted_successfully
            ].format(verb=verb_to_delete)
            flash(deleting_message, category="info")
        return redirect(url_for("phrasal_verbs_voc_ir.user_voc"))
    else:
        verb_vocabulary_actions.next_quest_sec_calcul()
        words_status_dict = verb_vocabulary_actions.test_objects_creating()
        # assert isinstance(words_status_dict, dict), ["The result object has wrong type. Not dict"]
        result = render_template("phrasal_verbs_voc_ir/phrasal_verbs_translator_ir.html",
                                 add_word_form=add_verb_form,
                                 delete_word_form=delete_verb_form,
                                 words_status_dict=words_status_dict,
                                 type=type, seconds_to_string=seconds_to_russian_string,
                                 )
        session["verb_translation_ir"] = None
        session["new_verb_ir"] = None
        return result


@phrasal_verbs_voc_ir.route("/show_user_voc_ir/<int:page_num>/<int:translation_available>",
                            methods=["POST", "GET"])
@login_required
def show_user_voc_ir(page_num, translation_available):
    verb_to_search_form = SearchPhrasalVerbForm(phrasal_verb=session.get("searching_verb_ir", ""))
    verb_vocabulary_actions = PhrasalVerbsVocabularyActionsIR(current_user)
    user_verbs_ir_pagin_obj_ir = verb_vocabulary_actions.show_user_verbs(page_num)
    result = render_template("phrasal_verbs_voc_ir/user_vocabulary_ir.html",
                             user_words_pagin_obj_ir=user_verbs_ir_pagin_obj_ir,
                             word_to_search_form=verb_to_search_form,
                             translation_available=translation_available,
                             abs=abs, seconds_to_string=seconds_to_russian_string,
                             )
    session["searching_verb_ir"] = ""
    session["searching_verb_translation_ir"] = ""
    return result


@phrasal_verbs_voc_ir.route("/search_user_verb/<int:page_num>/<int:translation_available>", methods=["GET", "POST"])
@login_required
def search_verb_user_voc(page_num, translation_available):
    verb_to_search_form = SearchPhrasalVerbForm(request.form)
    verb_to_search = verb_to_search_form.phrasal_verb.data
    if request.method == "POST" and verb_to_search_form.validate():
        verb_vocabulary_actions = PhrasalVerbsVocabularyActionsIR(current_user)
        searching_result = verb_vocabulary_actions.search_verb_in_user_voc(verb_to_search)
        if searching_result:
            session["searching_verb_ir"] = searching_result.key_word
            session["searching_verb_translation_ir"] = searching_result.translation
            session["searching_verb_description_ir"] = searching_result.description
            session["searching_verb_example_ir"] = searching_result.example
        else:
            search_message = flashed_messages_dict_phrs_vrb_ir[
                MessagesPhrasalVerbsIR.searching_phrs_verb_not_available
            ]
            flash(search_message, category="info")
    return redirect(url_for("phrasal_verbs_voc_ir.show_user_voc_ir", page_num=page_num,
                            translation_available=translation_available))


@phrasal_verbs_voc_ir.route("/near_verbs/<int:page_num>/<int:translation_available>",
                            methods=["POST", "GET"])
@login_required
def show_near_verbs(page_num=1, translation_available=0):
    verb_vocabulary_actions = PhrasalVerbsVocabularyActionsIR(current_user)
    near_verbs_pagin_obj = verb_vocabulary_actions.show_near_verbs(page_num)
    return render_template("phrasal_verbs_voc_ir/words_to_repeat.html",
                           near_words_pagin_obj=near_verbs_pagin_obj,
                           translation_available=translation_available,
                           abs=abs, seconds_to_string=seconds_to_russian_string,
                           )


@phrasal_verbs_voc_ir.route("/missing_verbs/<int:page_num>/<int:translation_available>",
                            methods=["POST", "GET"])
@login_required
def show_missing_verbs(page_num=1, translation_available=0):
    verb_vocabulary_actions = PhrasalVerbsVocabularyActionsIR(current_user)
    missing_verbs_pagin_obj = verb_vocabulary_actions.show_missing_verbs(page_num)
    return render_template("phrasal_verbs_voc_ir/words_to_repeat.html",
                           missing_words_pagin_obj=missing_verbs_pagin_obj,
                           translation_available=translation_available, abs=abs,
                           seconds_to_string=seconds_to_russian_string,
                           )


@phrasal_verbs_voc_ir.route("/lost_words/<int:page_num>/<int:translation_available>",
                            methods=["POST", "GET"])
@login_required
def show_lost_words(page_num=1, translation_available=0):
    verb_vocabulary_actions = PhrasalVerbsVocabularyActionsIR(current_user)
    lost_verbs_pagin_obj = verb_vocabulary_actions.show_lost_verbs(page_num)
    return render_template("phrasal_verbs_voc_ir/words_to_repeat.html",
                           lost_words_pagin_obj=lost_verbs_pagin_obj,
                           translation_available=translation_available,
                           abs=abs, seconds_to_string=seconds_to_russian_string,
                           )


@phrasal_verbs_voc_ir.route("/learned_words/<int:page_num>/<int:translation_available>",
                            methods=["POST", "GET"])
@login_required
def show_learned_words(page_num=1, translation_available=0):
    verb_vocabulary_actions = PhrasalVerbsVocabularyActionsIR(current_user)
    learned_words_pagin_obj = verb_vocabulary_actions.show_learned_verbs(page_num)
    return render_template("phrasal_verbs_voc_ir/words_to_repeat.html",
                           learned_words_pagin_obj=learned_words_pagin_obj,
                           translation_available=translation_available,
                           abs=abs, seconds_to_string=seconds_to_russian_string,
                           )


@phrasal_verbs_voc_ir.route("/drop_down_progress/<int:page_num>", methods=["POST", "GET"])
@login_required
def drop_down_progress(page_num):
    verb_vocabulary_actions = PhrasalVerbsVocabularyActionsIR(current_user)
    verb_vocabulary_actions.drop_down_progress(page_num)
    message_string = flashed_messages_dict_phrs_vrb_ir[MessagesPhrasalVerbsIR.lost_phrs_verb_progress_was_nullified]
    flash(message_string, category="info")
    return redirect(url_for("phrasal_verbs_voc_ir.user_voc", page_num=1,
                            translation_available=0))


if __name__ == "__main__":
    pass
