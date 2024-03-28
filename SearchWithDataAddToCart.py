import sqlite3

from flask import Flask, request, render_template, session

app: Flask = Flask(__name__, static_url_path='/static')
app.secret_key = "FelixPham"
#Mặc định gọi form search
@app.route('/')
def index():
    return render_template(
        'SearchWithCSSDataDBAddToCart.html', search_text="")

#Đối với phương thức Search
@app.route('/searchData', methods=['POST'])
def searchData():
    #Get data from Request
    search_text = request.form['searchInput']
    #Thay bang ham load du lieu tu DB
    html_table = load_data_from_db(search_text)
    print(html_table)
    return render_template('SearchWithCSSDataDBAddToCart.html',
                           search_text=search_text,
                           table=html_table
                           )


#Load dữ liệu và lọc ra bản ghi phù hợp
def load_data(search_text):
    import pandas as pd
    df = pd.read_csv('gradedata.csv')
    dfX = df
    if search_text != "":
        dfX = df[(df["fname"] == search_text) |
                 (df["lname"] == search_text)]
        print(dfX)
    html_table = dfX.to_html(classes='data',
                             escape=False)
    return html_table

def load_data_from_db(search_text):
        sqldbname = 'db/website.db'
        if search_text != "":
            # Khai bao bien de tro toi db
            conn = sqlite3.connect(sqldbname)
            cursor = conn.cursor()
            sqlcommand = ("Select * from storages "
                          "where model like '%")+search_text+ "%'"
            cursor.execute(sqlcommand)
            data = cursor.fetchall()
            conn.close()
            return data

    # Đối với phương thức Search
@app.route('/search', methods=['POST'])
def search():
    # Get data from Request
    search_text = request.form['searchInput']
    return render_template('SearchWithCSSDataDBAddToCart.html',
                           search_text=search_text)

@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    sqldbname = 'db/website.db'
    # 1. get the product id and quantity from the form
    product_id = request.form["product_id"]
    quantity = int(request.form["quantity"])
    # 2. get the product name and price from the database
    # or change the structure of shopping cart
    connection = sqlite3.connect(sqldbname)
    cursor = connection.cursor()
    cursor.execute("SELECT model, price "
                   "FROM storages WHERE id = ?",
                   (product_id,))
    # get one product
    product = cursor.fetchone()
    connection.close()
    # 3. create a dictionary for the product
    product_dict = {
        "id": product_id,
        "name": product[0],
        "price": product[1],
        "quantity": quantity
    }
    # 4. get the cart from the session or create an empty list
    cart = session.get("cart", [])

    # 5. check if the product is already in the cart
    found = False
    for item in cart:
        if item["id"] == product_id:
            #5.1update the quantity of the existing product
            item["quantity"] += quantity
            found = True
            break
    if not found:
            # 5.2. add the new product to the cart
        cart.append(product_dict)
    # 6. save the cart back to the session
    session["cart"] = cart
    rows = len(cart)
    outputmessage = "Product added to cart successfully! </br>Current: "+str(rows) + " products"
    # return a success message
    return outputmessage

@app.route("/cart")
def view_cart():
    # get the cart from the session or create an empty list
    # render the cart.html template and pass the cart
    current_cart = []
    if 'cart' in session:
        current_cart = session.get("cart", [])
    return render_template("cart.html", carts=current_cart)

if __name__ == '__main__':
    app.run(debug=True)


