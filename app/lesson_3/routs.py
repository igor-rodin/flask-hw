from flask import render_template
from app import app, db
from app.lesson_3.models import Student, Mark


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
    pass


@app.cli.command("init-db")
def init_db():
    db.drop_all()
    db.create_all()
    print("Ok")


@app.cli.command("fill-students-db")
def fill_students_db():
    student_1 = Student(
        first_name="Иванов", last_name="Иванов", email="ivan@example.com", group=24
    )
    student_2 = Student(
        first_name="Сергей", last_name="Петров", email="petr@example.com", group=24
    )
    student_3 = Student(
        first_name="Лена", last_name="Павлова", email="lena@example.com", group=32
    )
    student_4 = Student(
        first_name="Игорь", last_name="Иванов", email="igor@example.com", group=32
    )
    student_5 = Student(
        first_name="Михаил", last_name="Козлов", email="mikle@example.com", group=32
    )
    student_6 = Student(
        first_name="Вероника", last_name="Иванова", email="nika@example.com", group=24
    )

    mark_1 = Mark(class_name="Теория поля", value=4, student=student_3)
    mark_2 = Mark(class_name="Теория поля", value=5, student=student_4)
    mark_3 = Mark(class_name="Теория поля", value=4, student=student_5)
    mark_4 = Mark(class_name="История", value=4, student=student_4)
    mark_5 = Mark(class_name="История", value=5, student=student_3)
    mark_6 = Mark(class_name="История", value=5, student=student_5)
    mark_7 = Mark(class_name="Химия", value=4, student=student_1)
    mark_8 = Mark(class_name="Химия", value=3, student=student_2)
    mark_9 = Mark(class_name="Химия", value=5, student=student_6)
    mark_10 = Mark(class_name="Биология", value=3, student=student_1)
    mark_11 = Mark(class_name="Биология", value=4, student=student_2)
    mark_12 = Mark(class_name="Биология", value=4, student=student_6)
    mark_13 = Mark(class_name="Общая физика", value=4, student=student_1)
    mark_14 = Mark(class_name="Общая физика", value=5, student=student_2)
    mark_15 = Mark(class_name="Общая физика", value=4, student=student_6)
    mark_16 = Mark(class_name="Мат. анализ", value=4, student=student_4)
    mark_17 = Mark(class_name="Мат. анализ", value=5, student=student_3)
    mark_18 = Mark(class_name="Мат. анализ", value=3, student=student_5)

    db.session.add_all(
        [student_1, student_2, student_3, student_4, student_5, student_6]
    )
    db.session.add_all(
        [
            mark_1,
            mark_2,
            mark_3,
            mark_4,
            mark_5,
            mark_6,
            mark_7,
            mark_8,
            mark_9,
            mark_10,
            mark_11,
            mark_12,
            mark_13,
            mark_14,
            mark_15,
            mark_16,
            mark_17,
            mark_18,
        ]
    )
    db.session.commit()
