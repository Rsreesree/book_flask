
from flask import Flask, render_template, request, redirect,url_for
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sree@123'
app.config['MYSQL_DB'] = 'books'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

books = [{"id": 1, "title": "Python Crash Course", "author": "Eric Matthes" },
         {"id": 2, "title": "Automate the Boring Stuff with Python", "author": "Al Sweigart"}]


@app.route('/')
def index():
    
    return render_template('index.html',)

@app.route('/books')
def display_books():
    return render_template('books.html',books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    print("Request method:", request.method)
    if request.method == 'POST':
        print("Form data:", request.form)
        title = request.form.get('title')
        author = request.form.get('author')
        
        cur = mysql.connection.cursor()
        cur.execute("ALTER TABLE books AUTO_INCREMENT=3")
        cur.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
        books.append({"id": len(books) + 1, "title": title, "author": author})
        mysql.connection.commit()
        
        cur.close()

        return render_template('books.html', books=books)
    return render_template('add_books.html')

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return "Book not found", 404
    if request.method == 'POST':
        book['title'] = request.form['title']
        book['author'] = request.form['author']

        cur = mysql.connection.cursor()
        rows = cur.execute("UPDATE books SET title = %s, author = %s WHERE id = %s", (book['title'], book['author'], book_id))
        print(f"{rows} row(s) updated")
        print(book_id)
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('display_books'))
    return render_template('edit_book.html', book=book)

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    global books
    books = [book for book in books if book['id'] != book_id]
     
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM books WHERE id = %s", (book_id,))
    
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('display_books')) 

with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE TABLE books")
    mysql.connection.commit()
    cur.close()

if __name__ == 'main':
        app.run(debug=True)
