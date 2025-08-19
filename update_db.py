# from email import message
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, LargeBinary
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
import smtplib
import os
import glob
from datetime import date


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DATABASE


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diagrams.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class Diagrams(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    diagram: Mapped[str] = mapped_column(String, nullable=False)
    edit_date: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


path = 'static/figures'
now = date.today()

for item in glob.glob(os.path.join(path, '*.html')):
    file_name = item[15:].replace('.html', '')
    with open(item, 'r', encoding='utf-8') as file:
        file = file.read()
    with app.app_context():
        diagram = Diagrams(
            title=file_name,
            diagram=file,
            edit_date=f"{now.strftime("%d")} {now.strftime("%B")} {now.strftime("%Y")}",
        )
        db.session.add(diagram)
        db.session.commit()
