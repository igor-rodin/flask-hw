from app import db

# student_mark = db.Table(
#     "student_mark",
#     db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
#     db.Column("mark_id", db.Integer, db.ForeignKey("mark.id")),
# )


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    group = db.Column(db.Integer, nullable=False)
    marks = db.relationship("Mark", backref="student", lazy=True)

    def __repr__(self):
        return f"Student({self.first_name}, {self.last_name}, {self.email})"


class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_name = db.Column(db.String(80), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)

    def __repr__(self):
        return f"Mark({self.class_name}, {self.value})"
