from flask import Flask, render_template, redirect, url_for
from flask.helpers import make_response
from flask import request
from flask.json import jsonify
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisismyflasksecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbCoin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class coins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    news = db.Column(db.String(1000), nullable=True)
    
    def __repr__(self):
        return f"<coins {self.id}>"


@app.route('/')

def Page():

     if request.method == "POST":
        # здесь должна быть проверка корректности введенных данных
        try:
            p = coins(name=request.form['name'], news=request.form['news'])
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")
        return ''' 
                <html>
                <body>
                    <h1> Coin name <h1>
                    <form>
                        <p><input type="text" name="coinName" /></p>
                        <p><input type="submit" value="CHECK" /></p>
                    </form>
                </body>
            </html>'''

if __name__ == '__main__':
    
    app.run(debug=True)

