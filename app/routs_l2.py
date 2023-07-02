from flask import render_template, request, redirect, url_for, make_response
from app import app, csrf


@app.route("/lesson-2/")
def lesson_2():
    return render_template(
        "lesson-2/lesson-2.html", caption="Урок 2. Погружение во Flask"
    )


@app.route("/lesson-2/pow2/", methods=["GET", "POST"])
@csrf.exempt
def pow2():
    if request.method == "POST":
        result = None
        try:
            rqs = request.form.get("number")
            number = float(rqs)
            result, category = f"Квадрат числа {number} -> {number ** 2:.2f}", "success"
        except ValueError as e:
            result, category = (
                f"Должно быть целое или вещественное число (с точкой в качестве разделителя), получено {rqs}",
                "danger",
            )
        return render_template(
            "lesson-2/pow2.html",
            caption="Квадрат числа",
            result=result,
            category=category,
        )
    return render_template("lesson-2/pow2.html", caption="Квадрат числа")


@app.route("/lesson_2/login/", methods=["GET", "POST"])
@csrf.exempt
def login():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        response = make_response(redirect(url_for("welcome")))
        response.set_cookie("user_data", f"{name}:{email}")
        return response
    return render_template("lesson-2/login.html", caption="Регистрация")


@app.route("/lesson_2/welcome/")
def welcome():
    user_data = request.cookies.get("user_data")
    if user_data:
        user_name, email = user_data.split(":")
        return render_template(
            "lesson-2/welcome.html", user={"name": user_name, "email": email}
        )
    return redirect(url_for("login"))


@app.route("/lesson_2/logout/")
def logout():
    response = make_response(redirect(url_for("login")))
    response.set_cookie("user_data", "", expires=0)
    return response
