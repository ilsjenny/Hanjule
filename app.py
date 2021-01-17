from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


#    #    # 메인  #    #    #

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/books', methods=['GET'])
# 저장된 책, 이미지, 구절 불러오기 #
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


#   #    # 책추가  #    #    #

@app.route('/add_book')
def get_addbook_page():
    return render_template('add_book.html')

@app.route('/add_book', methods=['POST'])
# 책 정보 (제목, 이미지, 구절, 코멘트) 추가 #
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

#    #    #  책  #    #    #

@app.route('/book')
def get_book_page():
    book_id = request.args.get('book_id')
    return render_template('book.html', book_id=book_id)

@app.route('/book_quote', methods=['POST'])
# 구절 추가
def add_quote():
    quote_receive = request.form['quote_give']
    book_id = 'book_id 어떻게 찾지?'
    db.quotes.insert_one({
        'book_id': book_id,
        'quote': quote_receive,
    })

    return jsonify({'result': 'success', 'msg': '성공적으로 저장되었습니다.'})


@app.route('/book_comment', methods=['POST'])
# 코멘트 추가
def add_comment():
    comment_receive = request.form['comment_give']
    quote_id = 'quote_id 어떻게 찾지?'
    db.comments.insert_one({
        'quote_id': quote_id,
        'comment': comment_receive
    })

    return jsonify({'result': 'success', 'msg': '성공적으로 저장되었습니다.'})


@app.route('/bookpage', methods=['GET'])
# 책, 이미지, 구절, 코멘트 다 불러오기
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
                comment['quote_id'] = str(comment['quote_id'])

            quote['_id'] = str(quote['_id'])
            quote['comments'] = comments

        book['_id'] = str(book['_id'])
        book['quotes'] = quotes

    pprint(books)

    return jsonify({'result': 'success', 'books': books})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
