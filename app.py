from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# # # 홈페이지 연결  # # #
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/book')
def get_book_page():
    book_id = request.args.get('book_id')
    return render_template('book.html', book_id=book_id)


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

    book_insertion = db.books.insert_one({
        'title': title_receive,
        'image': image_receive
    })

    book_id = book_insertion.inserted_id

    quote_insertion = db.quotes.insert_one({
        'book_id': book_id,
        'quote': quote_receive,
    })

    quote_id = quote_insertion.inserted_id
    db.comments.insert_one({
        'quote_id': quote_id,
        'comment': comment_receive
    })

    return jsonify({'result': 'success', 'msg': '성공적으로 저장되었습니다.'})

@app.route('/book', methods=['POST'])
# 주어진 책에 구절 추가한 거 db에 저장하기 #
def add_quote():
    quote_receive = request.form['quote_give']
    book_id = '책 id'
    db.quotes.insert_one({
        'book_id': book_id,
        'quote': quote_receive,
    })
# 주어진 구절에 코멘트 추가한 거 db에 저장하기 #
def add_comment():
    comment_receive = request.form['comment_give']
    quote_id = '구절 id'
    db.comments.insert_one({
        'quote_id': quote_id,
        'comment': comment_receive
    })

@app.route('/book?', methods=['GET'])
#책, 이미지, 구절, 코멘트 보여주기
def read_book():
    books = list(db.books.find({}))
    for book in books:
        quotes = list(db.quotes.find({'book_id': book['_id']}))
        for quote in quotes:
            quote['_id'] = str(quote['_id'])
            quote['book_id'] = str(quote['book_id'])
            comments = list(db.comments.find({'quote_id': quote['_id']}))
            for comment in comments:
                comment['_id'] = str(comment['_id'])
                comment['quote_id']= str(comment['quote_id'])

    pprint(books)

    return jsonify({'result': 'success', 'books': books})

@app.route('/books', methods=['GET'])
# 저장된 책, 이미지, 구절 보여주기 #
def read_books():
    books = list(db.books.find({}))
    for book in books:
        quotes = list(db.quotes.find({'book_id': book['_id']}))
        for quote in quotes:
            quote['_id'] = str(quote['_id'])
            quote['book_id'] = str(quote['book_id'])

        book['_id'] = str(book['_id'])
        book['quotes'] = quotes

    pprint(books)

    return jsonify({'result': 'success', 'books': books})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
