from app import db
from bcrypt import hashpw, checkpw, gensalt


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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    birth_day = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    agreement = db.Column(db.Boolean, default=False)

    def set_password(self, password: str) -> str:
        salt = gensalt()
        self.password_hash = hashpw(
            salt=salt, password=password.encode("utf-8")
        ).decode("utf-8")

    def is_valid_password(self, password: str) -> bool:
        return checkpw(
            password.encode("utf-8"), hashed_password=self.password_hash.encode("utf-8")
        )

    def __repr__(self):
        return f"User({self.first_name} {self.last_name}, {self.email})"
