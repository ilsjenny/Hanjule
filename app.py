from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# # # 홈페이지 연결  # # #
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/book')
def get_book_page():
    return render_template('book.html')


@app.route('/quote')
def get_quote_page():
    return render_template('quote.html')


@app.route('/add_book')
def get_addbook_page():
    return render_template('add_book.html')


# # # # #

# 책 정보 (제목, 이미지, 구절, 코멘트) db에 저장하기 #
@app.route('/add_book', methods=['POST'])
def add_book():
    title_receive = request.form['title_give']
    image_receive = request.form['image_give']
    quote_receive = request.form['quote_give']
    comment_receive = request.form['comment_give']

    db.books.insert({
        'title': title_receive
        'image': image_receive
    })

    book_id = '책 id 값'
    db.quotes.insert({
        'book_id': book_id,
        'quote': quote_receive,
    })

    quote_id = '구절 id'
    db.comments.insert({
        'quote_id': quote_id,
        'comment': comment_receive
    })

    return jsonify({'result': 'success', 'msg': '성공적으로 저장되었습니다.'})

@app.route('/book', methods=['POST'])
# 주어진 책에 구절 추가한 거 db에 저장하기 #
def add_quote():
    quote_receive = request.form['quote_give']
    book_id = '책 id'
    db.quotes.insert({
        'book_id': book_id,
        'quote': quote_receive,
    })
# 주어진 구절에 코멘트 추가한 거 db에 저장하기 #
def add_comment():
    comment_receive = request.form['comment_give']
    quote_id = '구절 id'
    db.comments.insert({
        'quote_id': quote_id,
        'comment': comment_receive
    })

@app.route('/book', methods=['GET'])
def read_book():
# 저장된 책 보여주기 #
    book_id = '책 id 값'
    # 2. 책 검색 by id
    a_book = db.books.find_one({'_id': ObjectId(book_id)})
    a_book_id = str(a_book['_id']) # id 값 가져오는법
    # a_book_id == object_id (둘이 같은값임)
    # 2-1. api 결과값으로 objectId 넘기는법
    # b_book 딕셔너리 '_id' 키에 해당하는 값은 ObjectId 타입이라 API 결과값으로 보낼수가 없습니다.
    # 그래서 그걸 str 함수로 감싸서 문자열로 만들어줘야해요. 예를들어 find_one 으로 한개만 가져왔다면
    b_book = db.books.find_one({'_id': ObjectId(book_id)})
    b_book['_id'] = str(b_book['_id'])
# 저장된 구절 보여주기 #
    # 4. 문구들 검색 by book_id
    quotes = list(db.quotes.find({'book_id': book_id}))
# 저장된 코멘트 보여주기 #
    quote_id = '구절 id'  # 문자열
    comments = db.comments.find_one({'_id': quote_id})

@app.route('/', methods=['GET'])
# 저장된 책과 구절 보여주기 #
def read_books():
    books = db.books.find({})
    for book in books:
        book['_id'] = str(book['_id'])
    quotes = db.quotes.find({})
    for quote in quotes:
        quote['_id'] = str(quote['_id'])
    book_id = '책 id 값'
    quotes = list(db.quotes.find({'book_id': book_id}))
    return jsonify({'result': 'success', 'books': books})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
