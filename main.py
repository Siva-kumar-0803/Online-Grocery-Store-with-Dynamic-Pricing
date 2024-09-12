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
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/my account')
def my_account():
    return render_template('my account.html')

@app.route('/whishlist')
def whishlist():
    return render_template('whishlist.html')

@app.route('/add address')
def add_address():
    return render_template('add address.html')

@app.route('/products')
def product():
    return render_template('products.html')

@app.route('/single product')
def single_product():
    return render_template('single product.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')
@app.route('/shopping cart')
def shopping_cart():
    return render_template('shopping cart.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin customer details')
def admin_customer_details():
    return render_template('admin customer details.html')

@app.route('/admin order details')
def admin_order_details():
    return render_template('admin order details.html')


@app.route('/admin add product')
def admin_add_product():
    return render_template('admin add product.html')


if (__name__) == "__main__":
    app.run(debug=True)