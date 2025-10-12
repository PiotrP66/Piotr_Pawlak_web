from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
import smtplib
import os


# Find and load environment variables
dotenv_patch = find_dotenv()
load_dotenv(dotenv_patch)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap5(app)

# CREATE DATABASE


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DB_URI', 'sqlite:///diagrams.db')
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CONFIGURE TABLE


class Diagrams(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(
        String(250), nullable=False)
    diagram: Mapped[str] = mapped_column(String, nullable=False)
    edit_date: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

with app.app_context():
    diagram = db.session.execute(
        db.select(Diagrams.diagram).order_by(Diagrams.id))
    title = db.session.execute(
        db.select(Diagrams.title).order_by(Diagrams.id))
    all_diagrams = diagram.scalars().all()
    all_titles = title.scalars().all()
    diagrams_dict = {k: v for (k, v) in zip(all_titles, all_diagrams)}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/project_1')
def project_1():
    return render_template('project-1-details.html', fig=diagrams_dict)


@app.route('/project_2')
def project_2():
    return render_template('project-2-details.html')


@app.route('/project_3')
def project_3():
    return render_template('project-3-details.html')


@app.route('/project_4')
def project_4():
    return render_template('project-4-details.html')


@app.route('/send-email', methods=['POST'])
def send_mail():
    name = request.form.get('name')
    from_email = request.form.get('email')
    subject = request.form.get('subject')
    msg_body = request.form.get('message')

    msg = f'Subject: {subject}\n\nOd: {from_email}\nAuthor: {name}\n\nMessage:\n{msg_body}'
    print(msg_body)

    my_email = str(os.getenv('MY_EMAIL'))
    my_password = str(os.getenv('MY_PASSWORD'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email,
                             password=my_password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=my_email,
                                msg=msg.encode('utf-8'))
        return "OK"
    except Exception as e:
        return f"Błąd wysyłania wiadomości ({str(e)})"


if __name__ == "__main__":
    app.run(debug=True, port=5003)
