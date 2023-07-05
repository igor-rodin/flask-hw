from flask import render_template, redirect, url_for, flash
from app import app, db
from app.lesson_3.models import Student, Mark, User
from app.lesson_3.forms import RegisterForm
import json


@app.route("/lesson-3/")
def lesson_3():
    return render_template(
        "lesson-3/lesson-3.html", caption="Урок 3. Дополнительные возможности Flask"
    )


@app.route("/lesson-3/students/")
def students():
    students = db.session.scalars(db.select(Student)).all()
    return render_template(
        "lesson-3/students.html", caption="Список студентов", students=students
    )


@app.route("/lesson-3/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        birth_day = form.birthday.data
        email = form.email.data
        password = form.password.data
        agreement = form.agreement.data

        check_user = db.session.query(User).filter(User.email == email).first()
        if check_user:
            flash(
                "Такой email уже зарегистрирован. Попробуйте другой!", category="danger"
            )
            return redirect(url_for("register"))

        user = User(
            first_name=first_name,
            last_name=last_name,
            birth_day=birth_day,
            email=email,
            agreement=agreement,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return render_template("lesson-3/welcome.html", user=user)
    return render_template("lesson-3/register.html", caption="Регистрация", form=form)


@app.route("/welcome/")
def user_profile(user: str):
    return render_template("lesson-3/welcome.html", user=user)


@app.cli.command("init-db")
def init_db():
    db.drop_all()
    db.create_all()
    print("Ok")


@app.cli.command("fill-students-db")
def fill_students_db():
    json_file = app.config["STUDENTS_FILE"]

    with open(json_file, mode="r", encoding="utf-8") as f:
        students = json.load(f)

    for item in students:
        student = Student(
            first_name=item["first_name"],
            last_name=item["last_name"],
            email=item["email"],
            group=item["group"],
        )
        for mark in item["marks"]:
            student.marks.append(
                Mark(class_name=mark["class_name"], value=mark["value"])
            )
        db.session.add(student)
    db.session.commit()
