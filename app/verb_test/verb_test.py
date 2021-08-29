from flask import Blueprint, render_template, session, redirect, request, url_for, flash
from flask_security import current_user, login_required
from app.verb_test.working_test import VerbsTestCreator, check_answer
from app.verb_test.forms import AnswerForm
from app.models import LearnedPhrasalVerbs
from app.phrasal_verbs_voc_ir.phr_verbs_operations import MessagesPhrasalVerbsIR, flashed_messages_dict_phrs_vrb_ir

verb_test_bp = Blueprint("verb_test_bp", __name__, template_folder="templates",
                         static_folder="static"
                         )


@verb_test_bp.route("/pass_verbs_test/<verbs_test_type>/<int:words_count>")
@login_required
def pass_verbs_test(verbs_test_type: str, words_count: int = 10):
    test_checker = VerbsTestCreator(current_user)
    test_checker.words_count = words_count
    verbs_translations_list = test_checker.test_object_creating(verbs_test_type)
    session["verbs_test_type"] = verbs_test_type
    session["verbs_translations_list"] = verbs_translations_list
    session["right_answers_random_verbs_test"] = 0
    return redirect(url_for("verb_test_bp.verb_test", verb_number=0))


@verb_test_bp.route("/verb_test/<int:verb_number>", methods=["GET", "POST"])
@login_required
def verb_test(verb_number):
    test_checker_inst = VerbsTestCreator(current_user)
    answer_form = AnswerForm(request.form)
    is_successfully_learned = False
    test_len = len(session["verbs_translations_list"]) if session["verbs_translations_list"] else 0
    if not test_len:
        flash(flashed_messages_dict_phrs_vrb_ir[MessagesPhrasalVerbsIR.user_vocabulary_is_empty],
              category="info")
        return redirect(url_for("phrasal_verbs_voc_ir.user_voc"))
    if request.method == "POST":
        answer_to_check = answer_form.word.data.lower()
        right_answer = session["verbs_translations_list"][verb_number-1][1]
        checking_result = check_answer(answer_to_check, right_answer, sim=0.8)
        answer_form.word.data = ""
        if checking_result == "right":
            session["right_answers_random_verbs_test"] += 1
            if session["verbs_test_type"] in ("near_verbs", "missing_verbs"):
                successfully_repeated = test_checker_inst.verb_status_increment(
                    session["verbs_translations_list"][verb_number-1][5]
                )
                """Checks if the verb learning was passed all 7 stages, it means if the 
                 status equals 7. If not, successfully_repeated equals True"""
                is_successfully_learned = isinstance(successfully_repeated, LearnedPhrasalVerbs)
                """Here it needs to handle False result of verb_status_increment method
                It occurs if there is none of IntervalPhrasalVerbs association table.
                It means if user haven't any phrasal verbs in his personal table.
                But in this case executing 
                return redirect(url_for('phrasal_verbs_voc_ir.user_voc'))"""
        if verb_number >= test_len:
            return render_template("verb_test/verbs_test_result.html", test_len=test_len,
                                   checking_result=checking_result, round=round,
                                   word_number=verb_number, answer_form=answer_form,
                                   is_successfully_learned=is_successfully_learned
                                   )
    else:
        checking_result = None
        answer_form.word.data = ""
    return render_template("verb_test/verbs_test.html", test_len=test_len,
                           word_number=verb_number, answer_form=answer_form,
                           checking_result=checking_result, round=round,
                           is_successfully_learned=is_successfully_learned
                           )
