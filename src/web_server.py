import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class coins:

    def get_soup(self, coin_name):
        url = "https://coinmarketcap.com/currencies/" + coin_name + "/news/"
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        driver.get(url)
        time.sleep(3)
        for i in range(4):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)
            element = driver.find_element(By.XPATH, '//button[text()="Load More"]')
            driver.execute_script("arguments[0].click();", element)
            element.click()
            time.sleep(3)

        return BeautifulSoup(driver.page_source, "lxml")

    def get_paragraphs(self, coin_name):
        soup = self.get_soup(coin_name)
        news = soup.find_all("div", {"class": "svowul-5 czQlor"})
        ls = []
        for i in news:
            title = i.h3.text

            body = ""
            if (i.p):
                body = i.p.text

            link = i.a.get("href")
            if (link.startswith("/headlines/news/")):
                link = "https://coinmarketcap.com" + link

            ls.append({"title": title, "body": body, "link": link})

        return ls

    def output_paragraphs(self, coin_name):
        soup = self.get_soup(coin_name)
        news = soup.find_all("div", {"class": "svowul-5 czQlor"})
        num = 1
        for i in news:
            if (i.p):
                print(str(num) + ")     Title : " + i.h3.text + ".\n    Link: " + i.a.get("href"))
                print("Briefly: " + i.p.text)
                print(
                    "############################################################################################################")
                num += 1






class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coin_name = db.Column(db.String)
    title = db.Column(db.String)
    body = db.Column(db.String)
    link = db.Column(db.String)

    def __init__(self, coin_name, title, body, link):
        self.coin_name = coin_name
        self.title = title
        self.body = body
        self.link = link

    def __repr__(self):
        return '<Title %r>' % self.title


db.create_all()






@app.route("/coin", methods=['POST', 'GET'])
def coin():
    if request.method == 'POST':
        coin_name = request.form['coin'].lower()

        db_articles = News.query.filter_by(coin_name=coin_name).all()

        if (db_articles):
            return render_template('form.html', articles=db_articles)

        Coins = coins()
        articles = Coins.get_paragraphs(coin_name)

        for article in articles:
            db.session.add(News(coin_name, article['title'], article['body'], article['link']))

        db.session.commit()

        return ''' 
            <html>
                <body>
                    <h1> Coin name <h1>
                    <form>
                        <p><input type="text" name="name" /></p>
                        <p><input type="submit" value="CHECK" /></p>
                    </form>
                </body>
            </html>'''

    elif request.method == 'GET':
        return ''' 
            <html>
                <body>
                    <h1> Coin name <h1>
                    <form>
                        <p><input type="text" name="name" /></p>
                        <p><input type="submit" value="CHECK" /></p>
                    </form>
                </body>
            </html>'''


if __name__ == "__main__":
    app.run(debug=True)
