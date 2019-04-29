from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from werkzeug import secure_filename
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
import pandas as pd
 
application= app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = 'uploads/'

app.config['ALLOWED_EXTENSIONS'] = set(['pdf'])

def send_mail(mssg,toemail,subemail):
    msg = MIMEMultipart()
    message = mssg
    password = "12345pranab"
    msg['From'] = "developer.jalpaiguri@gmail.com"
    msg['To'] = toemail
    msg['Subject'] = subemail
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
message=' '
@app.route('/')
def home():
    if not session.get('logged_in'):
    	message="Welcome to our Portal!"
        flash(message)
        return render_template('login.html')
    else:
        return render_template('upload.html')
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    session['logged_in'] = False
    response = table.query(KeyConditionExpression=Key('email').eq(request.form['username']))
    passkey=''
    emailid=''
    for i in response['Items']:
        passkey=i['password']
        emailid=i['email']
    if request.form['password'] == passkey and request.form['username'] == emailid:
        session['logged_in'] = True
    else:
    	message="Please enter correct username and password!"
        flash(message)
        session['logged_in'] = False

    return home()

@app.route('/register', methods=['POST','GET'])
def register():
    return render_template('regsiter.html')

@app.route('/register_con', methods=['POST'])
def registerc():
    title = request.form['username']
    age = request.form['age']
    sex=request.form['gender']
    emailid=request.form['email address']
    passkey=request.form['password']
    response = table.put_item(Item={'username': title,'age': age,'sex':sex,'email':emailid,'password':passkey})
    txt_d='Thank you for the registration. Your Credentials for login are Email: {} and Password: {}'.format(emailid,passkey)
    send_mail(txt_d,emailid,'Registration of Account')
    new_dict={'username': title,'age': age,'sex':sex,'email':emailid}
    df=pd.DataFrame([new_dict])
    df.to_csv('temp.csv')
    return render_template('reg_sub.html')




@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            listp = os.listdir('uploads')
            number_files = len(listp)+1
            f_save=str(number_files)+'.pdf'            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_save))            
            filenames.append(filename)
            try:
            	d_y='uploads/'+f_save
            	s3.upload_file(d_y,'pranab1',f_save)
                response = table2.put_item(Item={'s3name':f_save,'originalname':filename,'up_det':str(datetime.datetime.now())})
            except:
            	pass
    return render_template('upload2.html', filenames=filenames)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
 
if __name__ == "__main__":
    s3 = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('pranab1')
    dynamodb2 = boto3.resource('dynamodb', region_name='us-east-1')
    table2 = dynamodb2.Table('pdetails')
    app.secret_key = os.urandom(12)
    app.run(port=9000)
