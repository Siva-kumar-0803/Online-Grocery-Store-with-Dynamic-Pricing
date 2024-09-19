from flask import Flask,render_template,redirect,request
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
mysql = MySQL(app)
bcrypt = Bcrypt(app)

# MySQL configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'grocery_store'

@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method == "POST" and "username" in request.form and "email" in request.form and "password" in request.form :
        name = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        cur = mysql.connection.cursor()

         # Check if email already exists
        cur.execute('SELECT email FROM customer WHERE email = %s', [email])
        db_email_data = cur.fetchall()

        if db_email_data:
            return "Email already exists"
        else:
            cur.execute('INSERT INTO customer (customer_name, email, password) VALUES (%s, %s, %s)', (name, email, hashed_password))
            mysql.connection.commit()

        cur.close()
        return redirect('/home')
    return render_template('signup.html')

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST" and "email" in request.form and "password" in request.form:
        email = request.form["email"]
        password = request.form["password"]
        cur = mysql.connection.cursor()
        cur.execute('SELECT password FROM customer WHERE email = %s', [email])
        fetching_email_password = cur.fetchone()
        print(fetching_email_password)
        if fetching_email_password:
            hashed_password = fetching_email_password[0]
            if bcrypt.check_password_hash(hashed_password, password):
                return redirect('/home')  # Redirect to the home page on successful login
            else:
                return "Incorrect password"
        else:
            return "Email does not exist"

        cur.close()
    return render_template('login.html')

@app.route('/home')
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

@app.route('/admin add product', methods=["GET", "POST"])
def admin_add_product():
    category = 0
    if request.method == "POST":
        # Function to read binary data is no longer necessary here.
        p_id = request.form['productId']
        
        # Ensure product_id is not empty
        if not p_id:
            return "Product ID is required!", 400  # Returning an error if productId is missing
        
        # Convert productId to integer if it's provided as a string
        try:
            p_id = int(p_id)
        except ValueError:
            return "Invalid Product ID. It should be an integer.", 400  # Erro
        name = request.form['productName']
        description = request.form['description']
        brand = request.form['brandName']
        price = request.form['price']
        expirydate = request.form["expiryDate"]
        quantity = request.form.get("weightquantity")
        stock = request.form['sku']
        ratings = request.form["rating"]
        nutritional_info = request.form["nutritionalInfo"]
        country = request.form["country"]
        categoryid = request.form['categoryId']
        category_name = request.form['categoryName']
        category_description = request.form['categoryDescription']

        if stock:
             availability = "available"

        # Retrieve the uploaded file
        if "image" in request.files:
            image_file = request.files["image"]
            image_data = image_file.read()  # This is already binary data
        else:
            # handle the case where no file was sent
            image_data = None


        if expirydate:
            try:
                # Parse the expiry date to ensure it's valid
                expirydate = datetime.strptime(expirydate, "%Y-%m-%d").date()
            except ValueError:
                # If the date is invalid, handle it here (e.g., set to None or return an error)
                expirydate = None
        else:
            # Set expirydate to None if it's empty
            expirydate = None


        # Insert the data into the database
        cur = mysql.connection.cursor()
        cur.execute('SELECT category_id FROM category WHERE category_id = %s', [categoryid])
        db_category_data = cur.fetchall()

        if categoryid not in db_category_data:
            cur.execute('INSERT INTO category (category_id,category_name,description) VALUES(%s,%s,%s)',(categoryid,category_name,category_description))
        
        if p_id and categoryid: 
            cur.execute('INSERT INTO products (product_id, product_name, price, brand_name, stock_keep_unit, expiry_date, weight_quantity, availability, ratings, neturitional_info, country, picture, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (p_id, name, price, brand, stock, expirydate, quantity, availability, ratings, nutritional_info, country, image_data, categoryid))
        mysql.connection.commit()
        cur.close()

    return render_template('admin add product.html')


if (__name__) == "__main__":
    app.run(debug=True)