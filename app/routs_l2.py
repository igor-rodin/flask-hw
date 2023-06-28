from flask import render_template, request, redirect, url_for
from app import app


@app.route("/lesson-2/")
def lesson_2():
    return render_template(
        "lesson-2/lesson-2.html", caption="Урок 2. Погружение во Flask"
    )


@app.route("/lesson-2/pow2/", methods=["GET", "POST"])
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
