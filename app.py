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

# 저장된 책, 이미지, 구절 불러오기 #
@app.route('/books', methods=['GET'])
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

# 책 정보 (제목, 이미지, 구절, 코멘트) 추가 #
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

    return jsonify({'result': 'success', 'msg': '저장되었습니다.'})

#    #    #  책  #    #    #

@app.route('/book')
def get_book_page():
    book_id = request.args.get('book_id')
    return render_template('book.html', book_id=book_id)

# 구절 추가
@app.route('/book_quote', methods=['POST'])
def add_quote():
    quote_receive = request.form['quote_give']
    book_id = request.form['book_id_give']
    db.quotes.insert_one({
        'book_id': ObjectId(book_id),
        'quote': quote_receive,
    })

    return jsonify({'result': 'success', 'msg': '저장되었습니다.'})

# 구절 & 해당 코멘트 삭제
@app.route('/book_quote_delete', methods=['POST'])
def delete_quote():
    quote_id = request.form['quote_id_give']
    db.quotes.delete_one({
        '_id': ObjectId(quote_id),
    })
    db.comments.delete_many({
        'quote_id': ObjectId(quote_id),
    })

    return jsonify({'result': 'success', 'msg': '삭제되었습니다.'})

# 코멘트 삭제
@app.route('/book_comment_delete', methods=['POST'])
def delete_comment():
    comment_id = request.form['comment_id_give']
    db.comments.delete_one({
        '_id': ObjectId(comment_id),
    })

    return jsonify({'result': 'success', 'msg': '삭제되었습니다.'})

# 책 & 구절 & 코멘트 삭제
@app.route('/book_delete', methods=['POST'])
def delete_all():
    book_id = request.form['book_id_give']
    db.books.delete_one({
        '_id': ObjectId(book_id)
    })
    quotes = db.quotes.find({
        'book_id': ObjectId(book_id),
    })
    for quote in quotes :
        db.comments.delete_many({
            'quote_id': quote['_id'],
        })

    db.quotes.delete_many({
        'book_id': ObjectId(book_id),
    })
    return jsonify({'result': 'success', 'msg': '삭제되었습니다.'})

# 코멘트 추가
@app.route('/book_comment', methods=['POST'])
def add_comment():
    comment_receive = request.form['comment_give']
    quote_id = request.form['quote_id_give']
    db.comments.insert_one({
        'quote_id': ObjectId(quote_id),
        'comment': comment_receive
    })

    return jsonify({'result': 'success', 'msg': '저장되었습니다.'})


# 책, 이미지, 구절, 코멘트 다 불러오기
@app.route('/bookpage', methods=['GET'])
def read_book():
    book_id = request.args.get('book_id')
    book = db.books.find_one({'_id': ObjectId(book_id)})

    quotes = list(db.quotes.find({'book_id': book['_id']}))

    for quote in quotes:
        comments = list(db.comments.find({'quote_id': quote['_id']}))
        quote['_id'] = str(quote['_id'])
        quote['book_id'] = str(quote['book_id'])
        for comment in comments:
            comment['_id'] = str(comment['_id'])
            comment['quote_id'] = str(comment['quote_id'])

        quote['_id'] = str(quote['_id'])
        quote['comments'] = comments

    book['_id'] = str(book['_id'])
    book['quotes'] = quotes

    pprint(book)

    return jsonify({'result': 'success', 'book': book})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
