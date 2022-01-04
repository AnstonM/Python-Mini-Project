from flask import *
import sqlite3
import os
from forms import *
from flask import flash 
from WikiReaper import *
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import *
from docx.shared import RGBColor
from docx.shared import Pt

topic='';fileName = '';heading = '';yourName = '';usn = '';sectionSize = 0;bodySize = 0;sectionAlignment = 0;bodyAlignment = 0;color = 0;underline = 0


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/index', methods=("GET","POST")) #TO RENDER INDEX PAGE
def index():
    global topic,fileName,heading,yourName,usn,sectionSize,bodySize,sectionAlignment,bodyAlignment,color,underline
    form = WikiReaperForm()
    if form.validate_on_submit():
        f = request.form
        topic = f['topic']
        fileName = f['fileName']
        heading = f['heading']
        yourName = f['yourName']
        usn = f['usn']
        sectionSize=int(form.sectionSize.data)
        bodySize=int(form.bodySize.data)
        sectionAlignment = int(form.sectionAlignment.data)
        bodyAlignment = int(form.bodyAlignment.data)
        color= int(form.color.data)
        underline= int(form.underline.data)
        return redirect(url_for('select'))
    else:
        return render_template('index.html',form=form)

@app.route('/select', methods=("GET","POST")) # TO RENDER SELECTION PAGE
def select():
    global topic,fileName,heading,yourName,usn,sectionSize,bodySize,sectionAlignment,bodyAlignment,color,underline
    try:
        max,sections = GetSections(topic)
    except:
        flash("Error in Retreiving the necessary data for your report, Try Again !!")
        return redirect(url_for('index'))
    form = SelectionForm()
    if form.validate_on_submit():
        f = request.form
        select = f['select']
        try:
            Addsection = GetSelection(max,sections,select)
        except:
            flash("Error in Selection, Check your Input...")
            return redirect(url_for('select'))
        if Addsection == [-1]:
            flash("Error in Selection, Check your Input...")
            return redirect(url_for('select'))
        try:
            headings,paragraphs = GetParagraphs(Addsection)
        except:
            flash("Error in Retreiving the necessary data for your report, Try Again !!")
            return redirect(url_for('index'))
        if paragraphs == [-1] or headings == [-1]:
            flash("Error in Retreiving the necessary data for your report, Try Again !!")
            return redirect(url_for('index'))
        try:
            MakeReport(headings,paragraphs,fileName,heading,yourName,usn,sectionAlignment,bodyAlignment,color,underline,sectionSize,bodySize)
        except:
            flash("Error in creating your report, Try Again !!")
            return redirect(url_for('index'))
        flash("Your Report Has been Successfully Created and downloaded to your Desktop , Enjoy !!!")
        return redirect(url_for('index'))
    else:
        return render_template('select.html',form=form,sections=sections)

@app.route('/CreateAccount', methods=("GET","POST"))
def CreateAccount():
    global userid
    form = CreateAccountForm()
    if form.validate_on_submit():
        f = request.form
        username = f['username']
        password = f['password']
        con = sqlite3.connect("ADP.db")
        cur = con.cursor()
        query = "INSERT INTO ACCOUNT(username,pwd) VALUES('"+username+"','"+password+"')"
        cur.execute(query)
        con.commit()
        con.close()
        flash("Account Successfully Created !!!")
        return redirect(url_for('login'))
    return render_template('AccountCreate.html',form=form)

@app.route('/')
@app.route('/login', methods=("GET","POST"))
def login():
    form = LoginForm()
    if form.validate_on_submit():        
        flash("Successfully Logged In")
        return redirect(url_for('index'))        
    else:       
        return render_template('login.html',form=form)

if __name__=='__main__':
    app.run(debug=True)