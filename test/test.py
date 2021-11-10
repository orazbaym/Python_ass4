from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class coins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    news = db.Column(db.String(1000), nullable=True)
    
    def __repr__(self):
        return f"<coins {self.id}>"



@app.route("/coins", methods=("POST", "GET"))
def register():
    if request.method == "POST":
        # здесь должна быть проверка корректности введенных данных
        try:
            p = coins(name=request.form['name'], news=request.form['news'])
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")

        return redirect(url_for('index'))

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


if __name__ == "__main__":
    app.run(debug=True)