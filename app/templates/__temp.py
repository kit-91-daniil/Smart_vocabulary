@app.route("/personal_room/show_user_voc/<login>/<int:page_num>", methods=["POST", "GET"])
@check_log
def show_user_voc(login, page_num):
    # result - это пагинационный объект
    result = inst.return_user_voc(page_num=page_num)
    if result:
        return render_template("user_voc.html", pagin_object=result, login=login)
    else:
        return render_template("user_voc.html", pagin_object=[], login=login,
                               note='Your vocabulary is empty')
