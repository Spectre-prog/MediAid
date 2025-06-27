from flask import Flask, flash, session, render_template, redirect, url_for, request, jsonify
import cloudinary
from cloudinary.uploader import upload
from config import *
from models import *
from flask_mail import Mail
from flask_migrate import Migrate
import fitz #this is for pymupdf, the pdf reader
from PIL import Image
import pytesseract
import tempfile
import io


app = Flask(__name__, template_folder='template', static_folder='static')

app.config.from_object(Config) #to configure all the configurations in config.py

#initializing the database
db.init_app(app)
mail = Mail(app)
migrate = Migrate(app, db)



@app.route('/')
def home():
    return render_template('home.html')

# Route handler for the login page
@app.route('/login', methods=['GET'])#this is to get the login page
def login_page():
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])#this deals with sending to the js
def api_login():
    user_data = request.get_json()
    email = user_data.get('email') #changed to email since we are working with js - Ugo 
    password = user_data.get('password') 
    
    # Query database for user
    user = User.query.filter_by(email=email).first()
    
    if user and user.check_password(password):  # In production, use proper password hashing for security
        session['user_id'] = user.id  # Store user ID in session just to keep track of logged-in user
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid email or password"})
    

@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@app.route('/api/signup', methods=['POST'])
def api_signup():
    new_user_data = request.get_json()
    name = new_user_data.get('name')
    email = new_user_data.get('email') 
    dob = new_user_data.get('dob')
    phonenumber = new_user_data.get('phonenumber')
    password = new_user_data.get('password')
    
    print("Received signup data:", new_user_data)
    print("Email:", email)
    print("Password:", password)
    
    if not email or len(password) < 6:
        return jsonify({"success": False, "message": "Invalid input"})

    if User.query.filter_by(email=email).first():  #check if user already exists with email
        return jsonify({"success": False, "message": "User already exists"})
        
    new_user = User( #create new user with all fields
        name = name,
        email = email,
        dob = dob,
        phonenumber = phonenumber,
        password = password
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Registration successful, please login"})

# Route handler for the dashboard (protected route)
@app.route("/user_dashboard")
def dashboard():
    if 'user_id' not in session:
        return jsonify({'success': True, 'message': 'Please login'})
        
    user = User.query.get(session['user_id'])
    return render_template('user_dashboard.html', user=user)

@app.route('/upload')
def file_upload():
    if 'user_id' not in session:
        return jsonify({'success': True, 'message': 'Please login'})
    
    if 'file' not in request.files: #this is for when no file was gotten from the frontend
        return jsonify({'success': False, 'message':'No file'})
    
    file = request.files['file']
    if file.filename == '': #this is when no file was chosen
        return jsonify({'success':False, 'message': 'No file has been chosen'})
    
    upload_file = upload(file) #this uploads the file to cloudinary
    file_url = upload_file.get('secure_url') #ths gets 

    new_doc = UserDocument(user_id = session['user_id'], file_url = file_url)
    db.session.add(new_doc)
    db.session.commit()

    return jsonify({'message': 'File uploaded', 'url': file_url})



# # route for AI testing interface
# @app.route('/ai-test', methods=['GET', 'POST'])
# def ai_test():
#     if request.method == 'POST':
#         if 'document' not in request.files:
#             return jsonify({'error': 'No document uploaded'}), 400
            
#         file = request.files['document']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400
            
#         if file:
#             try:
#                 # to be worked on ai doc processing
#                 result = {
#                     'filename': file.filename,
#                     'analysis': 'Analysis of your insurance document...'  # actual AI analysis
#                 }
#                 return jsonify(result)
#             except Exception as e:
#                 return jsonify({'error': str(e)}), 500
                
#     return render_template('ai_test.html')

@app.route('/my-document')
def my_docs():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login'})
    
    user_id = session['user_id']

    my_docs = UserDocument.query.filter_by(user_id=user_id).all()

    doc_urls = [my_doc.file_url for my_doc in my_docs ]

    return jsonify({'documents': doc_urls})


def extract_text_from_pdf(fle_bytes):
    

@app.route('/analyze/<int:doc_id')
def doc_analysis(doc_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login'})
    
    user_id=session['user_id']
    doc = UserDocument.query.filterby(id=doc_id, user_id=user_id)
    if not doc:
        return jsonify({'message': 'Document not found'}),404
    

        


@app.route('/logout')
def logout():
    session.clear()
    return jsonify({'message': 'Logout'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)

