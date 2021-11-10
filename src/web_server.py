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

url = "https://api.coinmarketcap.com/content/v3/news?coins=4030&page=1&size=5"

data = {
    'coins': '4030',
    'page': '1',
    'size': '5',
    }

Headers = {
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://coinmarketcap.com',
    'referer': 'https://coinmarketcap.com/',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform':'"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    }
    
def returnJsonRequest(url):
    r = requests.get(url,headers = Headers,params = data)
    return r.json()

def returnTitle(json):
    a = []
    for i in json['data']:
        a.append(i['meta']['title'])
    return a

def returnDesc(json):
    a = []
    for i in json['data']:
        a.append(i['meta']['subtitle'])
    return a

def printPage(a,b):
    for i in range(len(a)):
        print("\033[1m" , a[i] , "\033[0m",'\n')
        print("\t", b[i],'\n')
        print(".......................................................................", '\n')
    pass

printPage(returnTitle(returnJsonRequest(url)),returnDesc(returnJsonRequest(url)))

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

