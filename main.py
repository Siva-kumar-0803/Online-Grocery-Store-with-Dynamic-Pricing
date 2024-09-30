from flask import Flask,render_template,redirect,request,send_file
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from datetime import datetime
import io
import MySQLdb
import base64
from PIL import Image

app = Flask(__name__,static_folder='static')
mysql = MySQL(app)
bcrypt = Bcrypt(app)

# MySQL configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'grocery_store'


# mysql = MySQLdb.connect(
#     host=app.config['127.0.0.1'],
#     user=app.config['root'],
#     password=app.config['1234'],
#     db=app.config['grocery_store']
# )




def category():
    cur = mysql.connection.cursor()

    try:
        cur.execute("SELECT category_id, category_name, category_image FROM category")
        categories = cur.fetchall()

        # Debugging: Print out what categories contains

        category_list = []

        if categories:
            for category in categories:
                # Print each category for debugging

                # Ensure category has at least 3 elements
                if len(category) >= 3:
                    category_id = category[0]
                    category_name = category[1]

                    # Check if category_image is not None
                    if category[2] is not None:
                        category_image = base64.b64encode(category[2]).decode('utf-8')
                    else:
                        category_image = ''  # Handle missing image

                    category_list.append({
                        'id': category_id,
                        'name': category_name,
                        'image': category_image
                    })
                else:
                    return "Unexpected category structure: {category}"
        else:
            return "No categories found in the database."

    except Exception as e:
        return "Error fetching data: {e}"
    finally:
        return category_list
        cur.close()

def offers():
    cur = mysql.connection.cursor()

    try:
        cur.execute("SELECT offer_id, off_name, image FROM offers")
        offers = cur.fetchall()

        # Debugging: Print out what categories contains

        offers_list = []

        if offers:
            for offer in offers:
                # Print each category for debugging

                # Ensure category has at least 3 elements
                if len(offer) >= 3:
                    offer_id = offer[0]
                    offer_name = offer[1]

                    # Check if category_image is not None
                    if offer[2] is not None:
                        offer_image = base64.b64encode(offer[2]).decode('utf-8')
                    else:
                        offer_image = ''  # Handle missing image

                    offers_list.append({
                        'id': offer_id,
                        'name': offer_name,
                        'image': offer_image
                    })
                else:
                    return "Unexpected category structure: {offer}"
        else:
            return "No categories found in the database."

    except Exception as e:
        return "Error fetching data: {e}"
    finally:
        return offers_list
        cur.close()


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
    category_list = category()
    offers_list = offers()

    return render_template('home.html', categories=category_list, offers = offers_list)


@app.route('/home/offer')
def offer():
    cur = mysql.connection.cursor()

    try:
        cur.execute("SELECT offer_id, off_name, image FROM offers")
        offers = cur.fetchall()

        # Debugging: Print out what categories contains

        offers_list = []

        if offers:
            for offer in offers:
                # Print each category for debugging

                # Ensure category has at least 3 elements
                if len(offer) >= 3:
                    offer_id = offer[0]
                    offer_name = offer[1]

                    # Check if category_image is not None
                    if offer[2] is not None:
                        offer_image = base64.b64encode(offer[2]).decode('utf-8')
                    else:
                        offer_image = ''  # Handle missing image

                    offers_list.append({
                        'id': offer_id,
                        'name': offer_name,
                        'image': offer_image
                    })
                else:
                    print(f"Unexpected category structure: {offer}")
        else:
            print("No categories found in the database.")

    except Exception as e:
        print(f"Error fetching data: {e}")
    finally:
        cur.close()
    return render_template('home.html',offers=offers_list)



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


def date_convertor(var):
    if var:
            try:
                # Parse the expiry date to ensure it's valid
                date = datetime.strptime(var, "%Y-%m-%d").date()
                return date
            except ValueError:
                # If the date is invalid, handle it here (e.g., set to None or return an error)
                date = None
    else:
        # Set expirydate to None if it's empty
        date = None

def image_checker(var):
    if var:
        image_data = var.read()
        return image_data     
    else:
        # handle the case where no file was sent
        return None





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

        product_image = request.files["image"]
        image_data = image_checker(product_image)
        category_image = request.files["categoryImage"]
        image_data1 = image_checker(category_image)


        expirydate = date_convertor(expirydate)

        # Insert the data into the database
        cur = mysql.connection.cursor()
        cur.execute('SELECT category_id FROM category WHERE category_id = %s', [categoryid])
        db_category_data =  cur.fetchone()

        if not  db_category_data:
            cur.execute('INSERT INTO category (category_id,category_name,description,category_image) VALUES(%s,%s,%s,%s)',(categoryid,category_name,category_description,image_data1))
        
        if p_id and categoryid: 
            cur.execute('INSERT INTO products (product_id, product_name, price, brand_name, stock_keep_unit, expiry_date, weight_quantity, availability, ratings, neturitional_info, country, picture, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (p_id, name, price, brand, stock, expirydate, quantity, availability, ratings, nutritional_info, country, image_data, categoryid))
        mysql.connection.commit()
        cur.close()

    return render_template('admin add product.html')


@app.route('/admin add offers',methods=["GET","POST"])
def add_offer():
    if request.method == "POST":
        offer_id = request.form['offer_id']
        offer_name = request.form['offer_title']  
        offer_description = request.form['offer_description']
        start_date = date_convertor(request.form['start_date'])
        end_date = date_convertor( request.form['end_date'])
        discount_percentage = request.form['discount_percentage']
        off_img = request.files['offer_image']
        offer_image = image_checker(off_img)

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO offers (offer_id,off_name,off_desc,start_date,end_date,discount,image) VALUES(%s,%s,%s,%s,%s,%s,%s)',(offer_id,offer_name,offer_description,start_date,end_date,discount_percentage,offer_image))
        mysql.connection.commit()
        cur.close()

        
    
        

    return render_template('admin add offers.html')

if (__name__) == "__main__":
    app.run(debug=True)