from flask import Flask, render_template, request, url_for, flash, redirect
import pyodbc
from flask_mysqldb import MySQL
import pymssql
app = Flask(__name__)
app.secret_key = 'many random bytes'

db_server = 'DESKTOP-HME0A24'
db_name = 'GAR'
db_user = 'Venkat'
db_password = 'Password@123'
driver = '{SQL Server Native Client 11.0}'
conn = pymssql.connect(server=db_server, database=db_name,
                       user=db_user, password=db_password)


@app.route('/')
def home():
    return render_template('intro.html')


@app.route('/Index')
def Index():
    #     search_query = request.args.get('search_query', '')
    # cur = conn.cursor()
    # if search_query:
    #     cur.execute("SELECT * FROM rebootdb.LIST_TBL_QUESTIONNAIRE WHERE QUESTION_ID LIKE %s", ('%' + search_query + '%',))
    # else:
    #     cur.execute("SELECT * FROM rebootdb.LIST_TBL_QUESTIONNAIRE")
    # # cur.execute("SELECT * FROM rebootdb.LIST_TBL_QUESTIONNAIRE")
    # data = cur.fetchall()
    # cur.close()

    # return render_template('second.html', students=data, search_query=search_query)
    search_query = request.args.get('search_query', '')
    cur = conn.cursor()
    if search_query:
        cur.execute(
            "SELECT id,title,module,ACT.[order],location,primary_icon,caption,action_type,QUESTION_ID from rebootdb.activity as ACT WHERE module LIKE %s", ('%' + search_query + '%',))
    else:
        cur.execute(
            "SELECT id,title,module,ACT.[order],location,primary_icon,caption,action_type,QUESTION_ID FROM rebootdb.activity as ACT")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', students=data, search_query=search_query)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")

        title = request.form['title']
        module = request.form['module']
        order = request.form['order']
        Location = request.form['location']
        primary_icon = request.form['primary_icon']
        caption = request.form['caption']
        Action_type = request.form['action_type']
        Question_ID = request.form['question_id']
        cur = conn.cursor()
        cur.execute("INSERT INTO rebootdb.activity(title,module,[order],location,primary_icon,caption,action_type,Question_ID) VALUES (%s, %s, %s,%s,%s, %s, %s,%s)", (
            title, module, order, Location, primary_icon, caption, Action_type, Question_ID))

        conn.commit()

        return redirect(url_for('Index'))


@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = conn.cursor()
    cur.execute("DELETE FROM rebootdb.activity WHERE id=%s", (id_data,))
    conn.commit()
    return redirect(url_for('Index'))


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        module = request.form['module']
        # QUESTION=request.form['content']
        order = request.form['order']
        location = request.form['location']
        primary_icon = request.form['primary_icon']
        caption = request.form['caption'] 
        action_type=request.form['action_type']
        Question_ID = request.form['question_id'] # ---------
        # phone = request.form['phone']
        
        # cur = conn.cursor()
        # cur.execute("""
        # UPDATE rebootdb.LIST_TBL_QUESTIONNAIRE SET QUESTION_ID =%s,QUESTION_TYPE =%s,SEQUENCE =%s,IDENTIFIER =%s,QUESTION_TITLE  =%s,DETAIL_TEXT =%s,QUESTION =%s,ACTIVE  =%s,CONTENT_TYPE  =%s
        # WHERE id=%s
        # """, (Question_ID, Question_Type, sequence, Identifier, Question_title, Detail_Text, Question, Active, Content_type, id))
        # conn.commit()
        # flash("Data Updated Successfully")
        # return redirect(url_for('Second'))

        cur = conn.cursor()
        cur.execute("""
        UPDATE rebootdb.activity SET title=%s, module=%s,[order]=%s,[location]=%s,primary_icon=%s,caption=%s,action_type=%s,QUESTION_ID=%s
        WHERE id=%s
        """, (title, module,order,location,primary_icon,caption,action_type,Question_ID, id ))
        conn.commit()
        
        flash("Data Updated Successfully")
        
        return redirect(url_for('Index'))

# -----SECOND TABLE____


@app.route('/Second')
def Second():
    # search_query = request.args.get('search_query', '')  # Extract the search query from the URL parameters
    # cur = mysql.connection.cursor()  #it builds the connection between server and connection
    # if search_query:
    #     cur.execute("SELECT * FROM students WHERE email LIKE %s", ('%' + search_query + '%',))  # Perform the search operation
    # else:
    #     cur.execute("SELECT * FROM students") #if no search entry was executed this will be executed
    # data = cur.fetchall() #it fetches all the data from above two
    # cur.close() #here connection get cloosed
    # return render_template('index.html', students=data, search_query=search_query)
    search_query = request.args.get('search_query', '')
    cur = conn.cursor()
    if search_query:
        cur.execute("SELECT * FROM rebootdb.LIST_TBL_QUESTIONNAIRE WHERE QUESTION_ID LIKE %s",
                    ('%' + search_query + '%',))
    else:
        cur.execute("SELECT * FROM rebootdb.LIST_TBL_QUESTIONNAIRE")
    # cur.execute("SELECT * FROM rebootdb.LIST_TBL_QUESTIONNAIRE")
    data = cur.fetchall()
    cur.close()

    return render_template('second.html', students=data, search_query=search_query)


@app.route('/insertt', methods=['POST'])
def insertt():
    if request.method == "POST":
        flash("Data Inserted Successfully")

        # title = request.form['title']
        # module = request.form['module']
        # caption = request.form['caption']
        Question_ID = request.form['question_id']
        Question_Type = request.form['question_type']
        sequence = request.form['sequence']
        Identifier = request.form['Identifier']
        Question_title = request.form['question_title']
        Detail_Text = request.form['detail_text']
        Question = request.form['Question']
        Active = request.form['Active']
        Content_type = request.form['content_type']


        cur = conn.cursor()
        cur.execute("INSERT INTO rebootdb.LIST_TBL_QUESTIONNAIRE (QUESTION_ID,QUESTION_TYPE,SEQUENCE,IDENTIFIER,QUESTION_TITLE,DETAIL_TEXT,QUESTION,ACTIVE,CONTENT_TYPE) VALUES (%s, %s, %s,%s,%s, %s, %s,%s,%s)",
                    (Question_ID, Question_Type, sequence, Identifier, Question_title, Detail_Text, Question, Active, Content_type))

        conn.commit()

        return redirect(url_for('Second'))


@app.route('/deletee/<string:id_data>', methods=['GET'])
def deletee(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM rebootdb.LIST_TBL_QUESTIONNAIRE WHERE id=%s", (id_data,))
    conn.commit()
    return redirect(url_for('Second'))


@app.route('/updatee', methods=['POST', 'GET'])
def updatee():
    if request.method == 'POST':
        # id=request.form['id']
        # title = request.form['title']
        # module = request.form['module']
        id = request.form['id']
        Question_ID = request.form['question_id']
        Question_Type = request.form['question_type']
        sequence = request.form['sequence']
        Identifier = request.form['Identifier']
        Question_title = request.form['question_title']
        Detail_Text = request.form['detail_text']
        Question = request.form['question']
        Active = request.form['active']
        Content_type = request.form['content_type']

        # phone = request.form['phone']

        cur = conn.cursor()
        cur.execute("""
        UPDATE rebootdb.LIST_TBL_QUESTIONNAIRE SET QUESTION_ID =%s,QUESTION_TYPE =%s,SEQUENCE =%s,IDENTIFIER =%s,QUESTION_TITLE  =%s,DETAIL_TEXT =%s,QUESTION =%s,ACTIVE  =%s,CONTENT_TYPE  =%s
        WHERE id=%s
        """, (Question_ID, Question_Type, sequence, Identifier, Question_title, Detail_Text, Question, Active, Content_type, id))
        conn.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('Second'))

# ----Thrid TABLE----


@app.route('/Third')
def Third():

    # search_query = request.args.get('search_query', '')  # Extract the search query from the URL parameters
    # cur = mysql.connection.cursor()  #it builds the connection between server and connection
    # if search_query:
    #     cur.execute("SELECT * FROM students WHERE email LIKE %s", ('%' + search_query + '%',))  # Perform the search operation
    # else:
    #     cur.execute("SELECT * FROM students") #if no search entry was executed this will be executed
    # data = cur.fetchall() #it fetches all the data from above two
    # cur.close() #here connection get cloosed
    # return render_template('index.html', students=data, search_query=search_query)
    search_query = request.args.get('search_query', '')
    cur = conn.cursor()
    if search_query:
        cur.execute("SELECT * FROM [rebootdb].[LIST_TBL_QUESTIONNAIRE_ANSWER] where ID =%s",
                    (search_query))
    else:
        cur.execute("SELECT * FROM [rebootdb].[LIST_TBL_QUESTIONNAIRE_ANSWER]")
    # cur.execute("SELECT * FROM [rebootdb].[LIST_TBL_QUESTIONNAIRE_ANSWER]")
    data = cur.fetchall()
    cur.close()

    return render_template('third.html', students=data, search_query=search_query)


@app.route('/inserttt', methods=['POST'])
def inserttt():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        QUESTION_ID = request.form['question_id']
        SEQUENCE = request.form['sequence']
        VALUE = request.form['value']
        TEXT = request.form['text']
        ANSWER_VALUE = request.form['answer_value']
        ACTIVE = request.form['active']
        cur = conn.cursor()
        cur.execute("INSERT INTO [rebootdb].[LIST_TBL_QUESTIONNAIRE_ANSWER] ( QUESTION_ID, SEQUENCE, VALUE, TEXT, ANSWER_VALUE, ACTIVE) VALUES ( %s, %s, %s, %s, %s, %s)", (
            QUESTION_ID, SEQUENCE, VALUE, TEXT, ANSWER_VALUE, ACTIVE))

        conn.commit()

        return redirect(url_for('Third'))


@app.route('/deleteee/<string:id_data>', methods=['GET'])
def deleteee(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = conn.cursor()
    cur.execute("DELETE FROM [rebootdb].[LIST_TBL_QUESTIONNAIRE_ANSWER] WHERE id=%s", (id_data,))
    conn.commit()
    return redirect(url_for('Third'))


@app.route('/updateee', methods=['POST', 'GET'])
def updateee():
    if request.method == 'POST':
        ID = request.form['id']
        QUESTION_ID = request.form['question_id']
        SEQUENCE = request.form['sequence']
        VALUE = request.form['value']
        TEXT = request.form['text']
        ANSWER_VALUE = request.form['answer_value']
        ACTIVE = request.form['active']

        # phone = request.form['phone']

        cur = conn.cursor()
        cur.execute("""
        UPDATE [rebootdb].[LIST_TBL_QUESTIONNAIRE_ANSWER] SET  QUESTION_ID =%s, SEQUENCE =%s, VALUE =%s, TEXT =%s, ANSWER_VALUE =%s, ACTIVE =%s
        WHERE Id=%s
        """, ( QUESTION_ID, SEQUENCE, VALUE, TEXT, ANSWER_VALUE, ACTIVE, ID))
        conn.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('Third'))

if __name__ == "__main__":
    app.run(debug=True)
