from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.wycyfhs.mongodb.net/Cluster0?retryWrites=true&w=majority')
# client = MongoClient('mongodb+srv://test:sparta@cluster0.1sichzk.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    famous_receive = request.form['famous_give']
    star_receive = request.form['star_give']
    password_receive = request.form['password_give']

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property = "og:title"]')['content']
    image = soup.select_one('meta[property = "og:image"]')['content']
    description = soup.select_one('meta[property = "og:description"]')['content']

    all_movies = list(db.movies.find({}, {'_id': False}))
    if len(all_movies)==0 :
        key = 0
    else :
        key = all_movies[-1]['key']+1

    doc = {
        'key' : key,
        'title' : title,
        'image' : image,
        'description' : description,
        'famous' : famous_receive,
        'star' : star_receive,
        'password' : password_receive
    }
    db.movies.insert_one(doc)

    return jsonify({'msg':'저장 완료!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.movies.find({}, {'_id': False}))
    return jsonify({'movie': movie_list})

@app.route('/movieDetail')
def go_datail():
    return render_template('detail.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)