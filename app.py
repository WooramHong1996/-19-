from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi

ca = certifi.where()
# client = MongoClient('mongodb+srv://test:sparta@cluster0.wycyfhs.mongodb.net/Cluster0?retryWrites=true&w=majority')
client = MongoClient('mongodb+srv://test:sparta@cluster0.1sichzk.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
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
        'password' : password_receive,
        'comment' : []
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

@app.route("/comment/add", methods=["POST"])
def comment_add():
    key_receive = int(request.form['key_give'])
    new_comment = request.form['comment_give']
    search_movie = db.movies.find_one({'key': key_receive})
    print(search_movie)
    comment_list = search_movie['comment']

    comment_list.append(new_comment)
    db.movies.update_one({'key': key_receive}, {'$set': {'comment': comment_list}})

    return jsonify({'msg': '코멘트 추가 성공!'})



@app.route("/comment/del", methods=["POST"])
def comment_del():
    key_receive = int(request.form['key_give'])
    num_receive = int(request.form['num_give'])
    search_movie = db.movies.find_one({'key': key_receive})
    comment_list = search_movie['comment']

    del comment_list[num_receive]
    db.movies.update_one({'key': key_receive}, {'$set': {'comment': comment_list}})

    return jsonify({'msg': '댓글 삭제 완료!'})

@app.route("/change", methods=["POST"])
def chagne_star():
    key_receive = int(request.form['key_give'])
    pwd_receive = request.form['password_give']
    famous_receive = request.form['famous_give']
    star_receive = request.form['star_give']
    search_movie = db.movies.find_one({'key': key_receive})

    password = search_movie['password']
    if(pwd_receive==password):
        return
    comment_list = search_movie['comment']

    return jsonify({'msg': '댓글 삭제 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)