from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def get_main_page():
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

if __name__ == '__main__':
    app.run()
