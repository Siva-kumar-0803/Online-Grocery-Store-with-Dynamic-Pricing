from flask import Flask,render_template

app = Flask(__name__)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/my account')
def my_account():
    return render_template('account.html')

@app.route('/whishlist')
def whishlist():
    return render_template('whishlist.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')



if (__name__) == "__main__":
    app.run(debug=True)