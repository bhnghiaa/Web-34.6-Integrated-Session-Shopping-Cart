import sqlite3

from flask import Flask, request, render_template
app: Flask = Flask(__name__, static_url_path='/static')
#Mặc định gọi form search
@app.route('/')
def index():
    return render_template(
        'SearchWithCSSData.html', search_text="")

#Đối với phương thức Search
@app.route('/searchData', methods=['POST'])
def searchData():
    #Get data from Request
    search_text = request.form['searchInput']
    #Thay bang ham load du lieu tu DB
    html_table = load_data_from_db(search_text)
    print(html_table)
    return render_template('SearchWithCSSDataDB.html',
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
    return render_template('SearchWithCSSData.html',
                           search_text=search_text)
if __name__ == '__main__':
    app.run()


