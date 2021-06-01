from flask import Blueprint, render_template, session, redirect, request, url_for
from flask_security import current_user, login_required
from app.word_test.working_test import TestChecker, check_answer
from app.word_test.forms import AnswerForm

word_test_bp = Blueprint("word_test_bp", __name__, template_folder="templates",
                         static_folder="static"
                         )


@word_test_bp.route("/pass_test/<test_type>/<int:words_quantity>")
@login_required
def pass_test(test_type, words_quantity=10):
    test_checker_inst = TestChecker(current_user)
    test_checker_inst.words_quantity = words_quantity
    words_translations_list = test_checker_inst.test_object_creating(test_type)
    session["test_type"] = test_type
    session["words_translations_test"] = words_translations_list
    session["right_answers_random_test"] = 0
    return redirect(url_for("word_test_bp.word_test", word_number=0))


@word_test_bp.route("/word_test/<int:word_number>", methods=["GET", "POST"])
@login_required
def word_test(word_number):
    test_checker_inst = TestChecker(current_user)
    answer_form = AnswerForm(request.form)
    test_len = len(session["words_translations_test"])
    if request.method == "POST":
        success_learned = None
        answer_to_check = answer_form.word.data.lower()
        checking_result = check_answer(answer_to_check, word_number - 1, sim=0.8)
        answer_form.word.data = ""
        if checking_result == "right":
            session["right_answers_random_test"] += 1
            if session["test_type"] == "near" or \
                    session["test_type"] == "missing":
                success_learned = test_checker_inst.word_status_increment(
                    session["words_translations_test"][word_number-1][2]
                )
        if word_number >= test_len:
            return render_template("word_test/results_test.html", test_len=test_len,
                                   checking_result=checking_result, round=round,
                                   word_number=word_number, answer_form=answer_form,
                                   success_learned=success_learned
                                   )
    else:
        checking_result = None
        answer_form.word.data = ""
    return render_template("word_test/word_test.html", test_len=test_len,
                           word_number=word_number, answer_form=answer_form,
                           checking_result=checking_result, round=round
                           )
