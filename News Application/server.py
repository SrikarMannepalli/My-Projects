from flask import Flask,render_template, logging,request, flash,redirect,url_for,session
from flask_mysqldb import *
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from flask_mail import Mail,Message
import random
app=Flask(__name__)
app.config.from_pyfile('config.cfg')
mail=Mail(app)

#configuration
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Albus Dumbledore'
app.config['MYSQL_DB']='myFlaskApp'
app.config['MYSQL_CURSORCLASS']='DictCursor'
app.config['SESSION_PERMANENT']='False'
#initialization
mysql=MySQL(app)

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

class register(Form):
    name=StringField('NAME',[validators.Length(min=1)])
    username=StringField('USERNAME',[validators.Length(min=4)])
    email=StringField('EMAIL')
    password=PasswordField('PASSWORD',[validators.Length(min=4),validators.DataRequired(),
                                       validators.EqualTo('confirm',message='Passwords do not match')])
    confirm=PasswordField('CONFIRM PASSWORD')

class commen(Form):
    comment=StringField('COMMENT',[validators.Length(min=0)])

@app.route('/signup',methods=['GET','POST'])
def signup():
    form=register(request.form)
    if request.method=='POST' and form.validate():
        name_given= form.name.data
        username_given = form.username.data
        emailid_given=form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        check=0
        cur=mysql.connection.cursor()
        usernum = cur.execute('SELECT * FROM users WHERE id>%s',[0])
        id_to_give=usernum+1
        for name in cur:
            if name=={'username':username_given}:check=1
        if check==0:
            session['name']=name_given
            session['username']=username_given
            session['password']=password
            session['id']=id_to_give
            OTP=random.randint(1000,9999)
            session['OTP']=OTP
            msg=Message('Confirm e-mail',sender='dheerajreddy57@gmail.com',recipients=[emailid_given])
            msg.body='Your OTP is {}'.format(OTP)
            mail.send(msg)
            return redirect(url_for('verification'))

        else:
            flash("Please try again.A user with the same username already exists.",'danger')
        cur.close()
        return redirect(url_for('login'))
    return render_template('login.html',form=form)

@app.route('/verification',methods=['GET','POST'])
def verification():
    if request.method=='POST':
        OTP_given=request.form['otp']
        if int(OTP_given)==int(session['OTP']):
            cur=mysql.connection.cursor()
            usernum = cur.execute('SELECT * FROM users WHERE id>%s', [0])
            cur.execute("INSERT INTO users(id,name,username,password) VALUES(%s,%s,%s,%s)",
                        (session['id'],session['name'], session['username'], session['password']))
            usernum +=1
            new_user_table = "user" + str(usernum)
            cur.execute(
                "CREATE TABLE " + new_user_table + "(id INT(11) AUTO_INCREMENT PRIMARY KEY,heading VARCHAR(1000),"
                                                   "link VARCHAR(1000),imagelink VARCHAR(1000),imagewidth INT(11),"
                                                   "imageheight INT(11),article VARCHAR(10000))")
            flash('You have registered successfully', 'success')
            mysql.connection.commit()
        else:
            flash("You entered wrong OTP",'danger')
        return redirect(url_for('login'))
    return render_template('verification.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username_given = request.form['usernamelog']
        password_given = request.form['passwordlog']
        cur=mysql.connection.cursor()
        res=cur.execute('SELECT * FROM users WHERE username=%s',[username_given])
        if res>0:
            p_original=cur.fetchone()
            pass_original=p_original['password']
            id_original=p_original['id']
            if sha256_crypt.verify(password_given,pass_original):
                session['logged_in']=True
                session['username']=username_given
                session['id']=id_original
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong password.Please try again.", 'danger')
        else:
            flash("User with the given username does not exist does not exist.Please register before logging in.",'info')
        mysql.connection.commit()
        cur.close()
    return render_template('login.html')


@app.route('/logout')
def logout():
    print(session['username'])
    session.clear()
    flash("You have successfully logged out",'success')
    return redirect(url_for('dashboard'))


@app.route('/save/<x>/<y>',methods=['GET','POST'])
def save(x,y):
    try:
        if session['logged_in']==True:
            cur = mysql.connection.cursor()
            if y=="1":
                cur.execute("SELECT * FROM datatables")
            elif y=="2":
                cur.execute("SELECT * FROM dataindia")
            else:
                cur.execute("SELECT * FROM datacities")
            row = cur.fetchone()
            rowyo = row
            while row is not None:
                if row['id'] == int(x):
                    rowyo = row
                    break
                row = cur.fetchone()
            user_id=session['id']
            user_table="user"+str(user_id)
            res=cur.execute("SELECT * FROM "+user_table+" WHERE heading=%s",[rowyo['heading']])
            if res==0:
                cur.execute("INSERT INTO "+user_table+"(heading,link,imagelink,imagewidth,imageheight,article) VALUES(%s,%s,%s,%s,%s,%s)",
                            (rowyo['heading'],rowyo['link'],rowyo['imagelink'],rowyo['imagewidth'],rowyo['imageheight'],rowyo['article']))
                mysql.connection.commit()
            cur.close()

            return redirect(url_for('dashboard'))
    except:
        return redirect(url_for('login'))


@app.route('/Saved')
@app.route('/Saved/<x>/')
def Saved(x=None):
    cur=mysql.connection.cursor()
    user="user"+str(session['id'])
    cur.execute("SELECT * FROM " +user )
    if x is None:
        row=cur.fetchall()
        cur.close()
        return render_template('saved.html',rows=row)
    else:
        row=cur.fetchone()
        rowyo=row
        while row is not None:
            if row['id']==int(x):
                rowyo=row
                break
            row=cur.fetchone()
        cur.close()
        return render_template('shownews.html',rows=rowyo)

@app.route('/remove')
@app.route('/remove/<x>')
def remove(x=None):
    if x is not None:
        cur=mysql.connection.cursor()
        user="user"+str(session['id'])
        cur.execute("DELETE FROM "+user+" WHERE id=%s",[int(x)])
        mysql.connection.commit()
        return redirect(url_for('Saved'))
    else:
        return redirect(url_for('Saved'))


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    try:
        if session['logged_in']==True:
            cur=mysql.connection.cursor()
            cur.execute('SELECT * FROM datacities')
            rowc=cur.fetchall()
            cur.execute('SELECT * FROM datatables')
            rows=cur.fetchall()
            cur.execute('SELECT * FROM dataindia')
            rowi=cur.fetchall()
            rowso=zip(rows,rowc,rowi)
            return render_template('dashboard.html',rows=rowso,check=1)
    except:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM datacities')
        rowc = cur.fetchall()
        cur.execute('SELECT * FROM datatables')
        rows = cur.fetchall()
        cur.execute('SELECT * FROM dataindia')
        rowi = cur.fetchall()
        rowso = zip(rows, rowc, rowi)
        return render_template('dashboard.html', rows=rowso, check=2)


@app.route('/sports/')
@app.route('/sports/<x>/',methods=['GET','POST'])
def sports(x=None):
    try:
        if session['logged_in']==True:
            cur=mysql.connection.cursor()
            cur.execute("SELECT * FROM datatables")
            if x is None:
                rows = cur.fetchall()
                cur.close()
                return render_template('sports.html',rows=rows,check=1)
            else:
                form = commen(request.form)
                if request.method == 'POST' and form.validate():
                    comment_given = form.comment.data
                    cur = mysql.connection.cursor()
                    commented_user = session['username']
                    cur.execute("SELECT * FROM datatables")
                    rowc = cur.fetchone()
                    while rowc is not None:
                        if rowc['id'] == int(x):
                            rowyoc = rowc
                            break
                        rowc = cur.fetchone()
                    cur.execute("INSERT INTO commentstable(heading,username,comment) VALUES(%s,%s,%s)",
                                (rowyoc['heading'], commented_user, comment_given))
                    mysql.connection.commit()
                cur.execute('SELECT * FROM datatables')
                row = cur.fetchone()
                rowyo = row
                comments = []
                while row is not None:
                    if row['id'] == int(x):
                        rowyo = row
                        break
                    row = cur.fetchone()
                cur.execute('SELECT * FROM commentstable')
                rowco = cur.fetchone()
                while rowco is not None:
                    if rowco['heading'] == rowyo['heading']:
                        comments.append(rowco)
                    rowco = cur.fetchone()
                cur.execute("SELECT * FROM datatables")
                articledisplay=cur.fetchall()
                return render_template('shownews.html', rows=rowyo, form=form, comments=comments,check=1,articledisplay=articledisplay,category="sports")
    except:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM datatables")
        if x is None:
            rows = cur.fetchall()
            cur.close()
            return render_template('sports.html', rows=rows, check=2)
        else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM datatables')
            row = cur.fetchone()
            rowyo = row
            comments = []
            while row is not None:
                if row['id'] == int(x):
                    rowyo = row
                    break
                row = cur.fetchone()
            cur.execute('SELECT * FROM commentstable')
            rowco = cur.fetchone()
            while rowco is not None:
                print(rowco['heading'])
                if rowco['heading'] == rowyo['heading']:
                    comments.append(rowco)
                rowco = cur.fetchone()
                cur.execute("SELECT * FROM datatables")
                articledisplay = cur.fetchall()
            return render_template('shownews.html', rows=rowyo, comments=comments, check=2,articledisplay=articledisplay,category="sports")


@app.route('/india/')
@app.route('/india/<x>/',methods=['GET','POST'])
def india(x=None):
    try:
        if session['logged_in']==True:
            cur=mysql.connection.cursor()
            cur.execute("SELECT * FROM dataindia")
            if x is None:
                rows = cur.fetchall()
                cur.close()
                return render_template('india.html',rows=rows,check=1)
            else:
                form = commen(request.form)
                if request.method == 'POST' and form.validate():
                    comment_given = form.comment.data
                    cur = mysql.connection.cursor()
                    commented_user = session['username']
                    cur.execute("SELECT * FROM dataindia")
                    rowc = cur.fetchone()
                    while rowc is not None:
                        if rowc['id'] == int(x):
                            rowyoc = rowc
                            break
                        rowc = cur.fetchone()
                    cur.execute("INSERT INTO commentstable(heading,username,comment) VALUES(%s,%s,%s)",
                                (rowyoc['heading'], commented_user, comment_given))
                    mysql.connection.commit()
                cur.execute('SELECT * FROM dataindia')
                row = cur.fetchone()
                rowyo = row
                comments = []
                while row is not None:
                    if row['id'] == int(x):
                        rowyo = row
                        break
                    row = cur.fetchone()
                cur.execute('SELECT * FROM commentstable')
                rowco = cur.fetchone()
                while rowco is not None:
                    if rowco['heading'] == rowyo['heading']:
                        comments.append(rowco)
                    rowco = cur.fetchone()
                cur.execute("SELECT * FROM dataindia")
                articledisplay=cur.fetchall()
                return render_template('shownews.html', rows=rowyo, form=form, comments=comments,check=1,articledisplay=articledisplay,category="india")
    except:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM dataindia")
        if x is None:
            rows = cur.fetchall()
            cur.close()
            return render_template('india.html', rows=rows, check=2)
        else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM dataindia')
            row = cur.fetchone()
            rowyo = row
            comments = []
            while row is not None:
                if row['id'] == int(x):
                    rowyo = row
                    break
                row = cur.fetchone()
            cur.execute('SELECT * FROM commentstable')
            rowco = cur.fetchone()
            while rowco is not None:
                print(rowco['heading'])
                if rowco['heading'] == rowyo['heading']:
                    comments.append(rowco)
                rowco = cur.fetchone()
                cur.execute("SELECT * FROM dataindia")
                articledisplay = cur.fetchall()
            return render_template('shownews.html', rows=rowyo, comments=comments, check=2,articledisplay=articledisplay,category="india")

@app.route('/cities/')
@app.route('/cities/<x>/',methods=['GET','POST'])
def cities(x=None):
    try:
        if session['logged_in']==True:
            cur=mysql.connection.cursor()
            cur.execute("SELECT * FROM datacities")
            if x is None:
                rows = cur.fetchall()
                cur.close()
                return render_template('cities.html',rows=rows,check=1)
            else:
                form = commen(request.form)
                if request.method == 'POST' and form.validate():
                    comment_given = form.comment.data
                    cur = mysql.connection.cursor()
                    commented_user = session['username']
                    cur.execute("SELECT * FROM datacities")
                    rowc = cur.fetchone()
                    while rowc is not None:
                        if rowc['id'] == int(x):
                            rowyoc = rowc
                            break
                        rowc = cur.fetchone()
                    cur.execute("INSERT INTO commentstable(heading,username,comment) VALUES(%s,%s,%s)",
                                (rowyoc['heading'], commented_user, comment_given))
                    mysql.connection.commit()
                cur.execute('SELECT * FROM datacities')
                row = cur.fetchone()
                rowyo = row
                comments = []
                while row is not None:
                    if row['id'] == int(x):
                        rowyo = row
                        break
                    row = cur.fetchone()
                cur.execute('SELECT * FROM commentstable')
                rowco = cur.fetchone()
                while rowco is not None:
                    if rowco['heading'] == rowyo['heading']:
                        comments.append(rowco)
                    rowco = cur.fetchone()
                cur.execute("SELECT * FROM datacities")
                articledisplay=cur.fetchall()
                return render_template('shownews.html', rows=rowyo, form=form, comments=comments,check=1,articledisplay=articledisplay,category="cities")
    except:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM datacities")
        if x is None:
            rows = cur.fetchall()
            cur.close()
            return render_template('cities.html', rows=rows, check=2)
        else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM datacities')
            row = cur.fetchone()
            rowyo = row
            comments = []
            while row is not None:
                if row['id'] == int(x):
                    rowyo = row
                    break
                row = cur.fetchone()
            cur.execute('SELECT * FROM commentstable')
            rowco = cur.fetchone()
            while rowco is not None:
                if rowco['heading'] == rowyo['heading']:
                    comments.append(rowco)
                rowco = cur.fetchone()
                cur.execute("SELECT * FROM datacities")
                articledisplay = cur.fetchall()
            return render_template('shownews.html', rows=rowyo, comments=comments, check=2,articledisplay=articledisplay,category="cities")


@app.route('/other')
def other():
    try:
        if session['logged_in']==True:
            othrows = []
            dummy = []
            numyo = 1
            usernames=[]
            cur=mysql.connection.cursor()
            usernum = cur.execute('SELECT * FROM users WHERE id>%s', [0])
            cur.execute('SELECT * FROM users ')
            namerow=cur.fetchone()
            while namerow is not None:
                usernames.append(namerow)
                namerow=cur.fetchone()

            for ind in range(1,usernum+1):
                cur.execute("SELECT * FROM user"+str(ind))
                rows=cur.fetchall()
                othrows.append(rows)
                dummy.append(numyo)
                numyo+=1
            return render_template('otherusers.html',rows=othrows,dummy=dummy,usernames=usernames,check=1)
    except:
        othrows = []
        dummy = []
        numyo = 1
        usernames = []
        cur = mysql.connection.cursor()
        usernum = cur.execute('SELECT * FROM users WHERE id>%s', [0])
        cur.execute('SELECT * FROM users ')
        namerow = cur.fetchone()
        while namerow is not None:
            usernames.append(namerow)
            namerow = cur.fetchone()

        for ind in range(1, usernum + 1):
            cur.execute("SELECT * FROM user" + str(ind))
            rows = cur.fetchall()
            othrows.append(rows)
            dummy.append(numyo)
            numyo += 1
        return render_template('otherusers.html', rows=othrows, dummy=dummy, usernames=usernames, check=2)

if __name__=='__main__':
    app.secret_key='myflaskapp'
    app.debug=True
    app.run()

#error handling