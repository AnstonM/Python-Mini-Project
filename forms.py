from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from wtforms.validators import email_validator
import sqlite3
import re

alignmentList=[(0,'Left Align'),(1,'Center'),(2,'Right Align'),(3,'Justify')]
sizeList=[(4,4),(6,6),(8,8),(10,10),(12,12),(14,14),(16,16),(18,18),
    (20,20),(22,22),(24,24),(26,26),(28,28),(30,30),(32,32),(34,34),(36,36),
    (38,38),(40,40)]

colorList =[(0,'RED'),(1,'GREEN'),(2,'BLUE'),(3,'BLACK')]


class LoginForm(FlaskForm):

    def user_in(form,field):
        con = sqlite3.connect("ADP.db")
        print("Database successfully opened")
        cur = con.cursor()
        cur.execute("Select * from Account")
        rows = cur.fetchall()
        count = 0
        for rowdata in rows: 
            if field.data != rowdata[0]:
                count += 1
        if count == len(rows):
            raise ValidationError('UserName does not exist !!!')
        con.close()

    def valid_pass(form,field):
        con = sqlite3.connect("ADP.db")
        print("Database successfully opened")
        cur = con.cursor()
        cur.execute("Select * from Account")
        rows = cur.fetchall()
        count = 0
        for rowdata in rows: 
            if rowdata[0]==form.username.data:
                if rowdata[1]!=field.data:                    
                    raise ValidationError('Invalid Password !!!')        
        con.close()

    username = StringField('User Name',[DataRequired(),user_in])
    password = PasswordField('Password',[DataRequired(),valid_pass])
    submit = SubmitField(label='SIGN IN',)

class CreateAccountForm(FlaskForm):
    
    def username_nottaken(form,field):
        con = sqlite3.connect("ADP.db")
        print("Database successfully opened")
        cur = con.cursor()
        cur.execute("Select * from Account")
        rows = cur.fetchall()
        count = 0
        for rowdata in rows: 
            if field.data == rowdata[0]:
                raise ValidationError(message='UserName is Taken !!!')
        con.close()
        

    def valid_pass(form,field):
        count = 0
        if len(field.data) >= 8:
            count += 1
        if not field.data.isalnum() and not field.data.isupper() and not field.data.islower() and not field.data.isdecimal():
            count += 1
        if count != 2:
            raise ValidationError(message='>= 8 characters, must contain \nA-Z or a-Z ,0-9 ,\na special character( !,@,#,$,%,^,&,* )')
    
    username = StringField('User Name',[DataRequired(),username_nottaken])
    password = PasswordField('Password',[DataRequired(),valid_pass])
    confirmpassword = PasswordField('Confirm\nPassword',[DataRequired(),EqualTo('password',message="Password doesn't match")])
    submit = SubmitField(label="CREATE ACCOUNT")    

class WikiReaperForm(FlaskForm):

    def valid_name(form,field):
        dataList = field.data.split(' ')
        for i in dataList:
            if not i.isalpha() :
                raise ValidationError('Name should contain alphabets only !!!') 
    
    def valid_usn(form,field):
       regex = re.compile(r'[\d][\w]{2}[\d]{2}[\w]{2}[\d]{3}')
       result = regex.search(field.data)
       if result == None:
           raise ValidationError(message='Invalid USN')

    def valid_topic(form,field):
        dataList = field.data.split(' ')
        for i in dataList:
            if not i.isalnum():
                raise ValidationError('Topic cant contain special characters!!!') 
        
    topic=StringField("Report On:",[DataRequired(),valid_topic])
    fileName = StringField("Output File Name:",[DataRequired()])
    heading = StringField("Report Title:",[DataRequired()])
    yourName = StringField("Your Name:",[DataRequired(),valid_name])
    usn = StringField('Your USN:',[DataRequired(),valid_usn],render_kw={"placeholder": "Eg. 4SO17CS089"})
    sectionSize = SelectField('Heading Font Size:',choices=sizeList,default=26)
    bodySize = SelectField('Body Font Size:',choices=sizeList,default=14)
    sectionAlignment = SelectField('Heading Alignment:',choices=alignmentList,default=0)
    bodyAlignment = SelectField('Body Alignment:',choices=alignmentList,default=0)
    color = SelectField('Heading Color:',choices=colorList,default=3)
    underline = RadioField('Underline for Heading:', choices=[(1,'Underlined Heading'),(0,'Plain Heading')],default=0)
    submit = SubmitField(label='CONTINUE') 
    
class SelectionForm(FlaskForm):

    select = StringField("Topics to be Included : ",[DataRequired()],render_kw={"placeholder": "Eg. 5,8 or 4-8"})
    submit = SubmitField(label='CREATE REPORT') 