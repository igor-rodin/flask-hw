from flask import render_template
from app import app


@app.route("/lesson-2")
def lesson_2():
    return render_template(
        "lesson-2/lesson-2.html", caption="Урок 2. Погружение во Flask"
    )
