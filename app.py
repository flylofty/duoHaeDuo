from flask import Flask, render_template, request, jsonify
from datetime import datetime
from pymongo import MongoClient

client = MongoClient('mongodb+srv://junho:sparta@cluster0.4iq35.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/write')
def get_write_page():
    return render_template('write_page.html')


@app.route("/write", methods=["POST"])
def save_write():

    # 클라이언트 요청 데이터
    tier_receive = request.form['tier_give']
    rating_receive = request.form['rating_give']
    date_receive = get_duo_date(request.form['date_give'])
    content_receive = request.form['content_give']

    # 작성된 시간 얻기
    today = datetime.now()
    date_time = today.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")

    # db.write_count 에 저장된 유일한 값을 가져옴 => 게시글 고유 id로 사용
    write_count = list(db.write_count.find({}, {'_id': False}))[0]['count'] + 1

    # DB 데이터 생성
    doc = {
        'id': write_count,           # 게시글 고유 아이디
        'tier': tier_receive,        # 티어 정보
        'rating': rating_receive,    # 등급 정보
        'duo_date': date_receive,    # 듀오 하고 싶은 시간 정보
        'content': content_receive,  # 어필 내용
        'date_time': date_time       # 게시글 작성 시간
    }

    # DB 데이터 저장
    db.lol_collection.insert_one(doc)

    # 유일한 값 증가
    db.write_count.update_one({'count': int(write_count - 1)}, {'$set': {'count': write_count}})

    return jsonify({'msg': '등록 완료!'})


def get_duo_date(data):
    # 듀오할 시간 구하기 문자 예쁘게 만들기
    temp_date = data.split('T')
    ymd = temp_date[0].split('-')
    hs = temp_date[1].split(':')

    hour = int(hs[0])

    if hour >= 20:
        pm_am_info = '저녁'
    elif hour >= 12:
        pm_am_info = '오후'
    elif hour >= 6:
        pm_am_info = '오전'
    else:
        pm_am_info = '새벽'

    if hour > 12:
        hour -= 12

    # 2022년 05월 10일 13시 20분
    duo_date = f'{ymd[0]}년 {ymd[1]}월 {ymd[2]}일 {pm_am_info} {hour}시 {hs[1]}분'
    return duo_date


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
