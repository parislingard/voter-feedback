from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@127.0.0.1/vote'

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ajjnimyalqjngb:bda2e8560f0d2ac5fe6cf894996044172e65e4ba1bb341856d59b310ecf8939d@ec2-3-215-207-12.compute-1.amazonaws.com:5432/ddk6oae6hllkj3'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    ___tablename___ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    voter = db.Column(db.String(200), unique=True)
    pollsite = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, voter, pollsite, rating, comments):
        self.voter = voter
        self.pollsite = pollsite
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        voter = request.form['voter']
        pollsite = request.form['pollsite']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(voter, pollsite, rating, comments)
        if voter == '' or pollsite == '':
            return render_template('index.html', message="Please enter required fields")
        if db.session.query(Feedback).filter(Feedback.voter == voter).count() == 0:
            data = Feedback(voter, pollsite, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(voter, pollsite, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message="You have already submitted feedback")

if __name__ == '__main__':
    app.run()
