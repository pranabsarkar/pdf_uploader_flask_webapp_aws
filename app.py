import os
from werkzeug import secure_filename
from flask import Flask
from flask import flash
from flask import send_from_directory
from flask import render_template
from flask import request
from flask import session
from src.process import Process
 
application= app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['pdf'])

process_client = Process()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    if not session.get('logged_in'):
    	message="Welcome to our Portal!"
        flash(message)
        return render_template('login.html')
    else:
        return render_template('upload.html')
 
@app.route('/login', methods=['POST'])
def user_login():
    try:
        session['logged_in'] = False
        response = process_client.database_process.search_item_user_db(email_address=request.form['email address'])
        if response['password'] == request.form['password'] and response['email_address'] == request.form['email address']:
            session['logged_in'] = True
        else:
            message="Please enter correct username and password!"
            flash(message)
            session['logged_in'] = False
    except Exception as e:
        print(e)
    else:
        return home()

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    process_client.user_sign_up(
        user_name=request.form['username'],
        age=request.form['age'],
        gender=request.form['gender'],
        email_address=request.form['email address'],
        password=request.form['password']
    )
    return render_template('reg_sub.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/upload', methods=['POST'])
def upload():
    try:
        uploaded_files = request.files.getlist("file[]")
        filenames = []
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                list_files = os.listdir('uploads')
                f_save=str(len(list_files)+1)+'.pdf'            
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_save))            
                filenames.append(filename)
                key_name='uploads/'+f_save
                process_client.storage_process.upload_file(key_name,'pranab1',f_save)
                process_client.database_process.insert_item_into_storage_db(
                    s3_key_name=key_name,
                    original_name=filename
                )
    except Exception as e:
        print(e)
    else:
        return render_template('upload_file.html', filenames=filenames)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename
    )
 
if __name__ == "__main__":
    try:
        app.secret_key = os.urandom(12)
        app.run(debug=True, port=9000)
    except Exception as e:
        print(e)