from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'fisat pro'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '007'
app.config['MYSQL_DB'] = 'flaskapp'

mysql = MySQL(app)

@app.route('/')
def index():
    return "hello flask is connected to mysql"

if __name__ == '__main__':
    app.run(debug=True)




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        if user and check_password_hash(user['password'], password):
            return redirect(url_for('index'))
        else:
            return "Invalid username or password"
    return render_template('login.html')
@app.route('/users')
def users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, username FROM users")
    user_list = cursor.fetchall()
    print(user_list)
    cursor.close()
    return render_template('users.html', users=user_list)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        new_username = request.form['username']
        cursor.execute("UPDATE users SET username = %s WHERE id = %s", (new_username, id))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('users'))
    cursor.execute("SELECT * FROM users WHERE id = %s", [id])
    user = cursor.fetchone()
    cursor.close()
    return render_template('edit.html', user=user)

@app.route('/delete/<int:id>')
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", [id])
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('users'))















