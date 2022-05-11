from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:test@cluster0.uyqla.mongodb.net/cluster0?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')




@app.route("/board/<int:id>", methods=["GET"])
def get_board(id):
    # lol_collection 은 본인이 쓰는 콜렉션 가져다 붙이면 됩니다~!
    # DB에게 요청 => db.lol_collection.find_one({'id': write_id}, {'_id': False})
    # 응답 받은 데이터 => data
    data = db.lol_collection.find_one({'id': id}, {'_id': False})

    # data 는 DB에 저장된 정보를 가져온 것이고 아래와 같은 데이터 입니다
    # sample_data = {
    #     'id': 1,                                       # 게시글 번호
    #     'tier': '브론즈',                               # 티어 정보
    #     'rating': '3',                                 # 등급 정보
    #     'duo_date': '2022년 05월 10일 오후 1시 21분',     # 듀요 하고 싶은 시간
    #     'content': 'ㄱㄱㄱㄱㄱ',                         # 게시글 내용 (어필 내용)
    #     'date_time': '2022년 05월 10일 21시 59분 04초'    # 게시글 작성 시간
    # }
    print(data)
    # article_id = data['id']
    tier = data['tier']
    rating = data['rating']
    content = data['content']
    duo_date = data['duo_date']
    image_url = db.tier_image.find_one({'tier': tier}, {'_id': False})['image_url']


    # Jinja 에서는 writer[0], writer[1], writer[2], writer[3]
    # {% set tier = writer[0] %}
    # {% set rating = writer[1] %}
    # {% set content = writer[2] %}
    # {% set duo_date = writer[3] %}
    writer = [tier, rating, content, duo_date, image_url]

    return render_template("board.html", writer=writer)


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)
