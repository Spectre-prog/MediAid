from flask import Flask, flash, session, render_template, redirect, url_for, request, jsonify
from cloudinary.uploader import upload
from config import Config
from models import db, User, InsuranceDocument
import json
from flask_mail import Mail, Message
import random
import os

# Initialize Flask application
app = Flask(__name__, template_folder='template', static_folder='static')

# Configure database settings from Config class
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

# Initialize database with app
db.init_app(app)


# Secret key for session management (required for flash messages), you can decide to remove them.
app.secret_key = os.environ.get('SECRET_KEY')  # Secret key from .env file


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'projectfinodido@gmail.com'
app.config['MAIL_PASSWORD'] = 'csqv yavo jcwj bghz'  # email password
app.config['MAIL_DEFAULT_SENDER'] = 'projectfinodido@gmail.com'  # 
 # app password
mail = Mail(app)
# Route handler for the home page
@app.route('/')
def home():
    """
    Handle requests to the root URL ('/').
    Renders the home page template.
    
    Returns:
        rendered template: home.html with any necessary context
    """
    return render_template('home.html')

# Route handler for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle both GET and POST requests to /login.
    GET: Display login form 
    POST: Process login form submission
    
    Returns:
        GET: rendered login.html template
        POST: redirect to dashboard on success or back to login on failure
    """
    if request.method == 'POST':
        # Get form data from login.html form
        email = request.form.get('login-email') # Changed to match login-email input ID
        password = request.form.get('login-password') # Changed to match login-password input ID
        
        # Query database for user
        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password:  # In production, use proper password hashing for security
            session['user_id'] = user.id  # Store user ID in session just to keep track of logged-in user
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

# Route handler for the signup page
# ...existing code...

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided!'}), 400

        full_name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        dob = data.get('dob')
        password = data.get('password')
        language = data.get('language')

        if not email:
            return jsonify({'error': 'Email is required!'}), 400

        otp = str(random.randint(100000, 999999))

        session['pending_user'] = {
            'full_name': full_name,
            'phone': phone,
            'email': email,
            'dob': dob,
            'password': password,
            'language': language,
            'otp': otp
        }

        try:
            msg = Message('Your MediAid OTP', sender='your_email@gmail.com', recipients=[email])
            msg.body = f"Your OTP is: {otp}"
            mail.send(msg)
        except Exception as e:
            return jsonify({'error': f'Failed to send OTP: {str(e)}'}), 500

        # Render the OTP page directly after sending OTP
        return render_template('otp_verify.html', email=email)

from flask import request, jsonify, render_template, session, redirect, url_for

@app.route('/otp_verify', methods=['GET', 'POST'])
def otp_verify():
    if request.method == 'GET':
        # Render the OTP input page
        email = request.args.get('email')
        lang = request.args.get('lang')
        return render_template('otp_verify.html', email=email, lang=lang)

    try:
        # Support both JSON (AJAX) and form POST
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        input_otp = data.get('otp')
        if not input_otp:
            return jsonify({'error': 'OTP is required'}), 400

        if 'pending_user' not in session:
            return jsonify({'error': 'No OTP in session'}), 400

        user_data = session['pending_user']

        if input_otp != user_data['otp']:
            return jsonify({'error': 'Incorrect OTP'}), 400

        # Check if user already exists
        if User.query.filter_by(email=user_data['email']).first():
            return jsonify({'error': 'User already exists'}), 400

        # Save to DB
        new_user = User(
            full_name=user_data.get('full_name'),
            phone=user_data.get('phone'),
            email=user_data.get('email'),
            dob=user_data.get('dob'),
            password=user_data.get('password'),  # Hash in production!
            language=user_data.get('language')
        )
        db.session.add(new_user)
        db.session.commit()

        # Clear session
        session.pop('pending_user')

        # If form POST, redirect to login or dashboard
        if not request.is_json:
            return redirect(url_for('login'))

        return jsonify({'message': 'User created successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# Route handler for the dashboard (protected route)
@app.route("/template/user_dashboard")
def dashboard():
    """
    Protected route for authenticated users.
    Requires user to be logged in.
    
    Returns:
        rendered dashboard template if authenticated
        redirect to login if not authenticated
    """
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
        
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

# Route for logging out
@app.route('/logout')
def logout():
    """
    Handle user logout by clearing session.
    
    Returns:
        redirect to home page
    """
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

# route for AI testing interface
@app.route('/ai-test', methods=['GET', 'POST'])
def ai_test():
    if request.method == 'POST':
        if 'document' not in request.files:
            return jsonify({'error': 'No document uploaded'}), 400
            
        file = request.files['document']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        if file:
            try:
                # to be worked on ai doc processing
                result = {
                    'filename': file.filename,
                    'analysis': 'Analysis of your insurance document...'  # actual AI analysis
                }
                return jsonify(result)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
                
    return render_template('ai_test.html')

# Run the application
if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
    # Start development server    
    app.run(debug=True)


# Frontend Route Guide:
# -------------------
# / (GET)
#     - Home page route
#     - Displays the main landing page
#     - Public access
# /login (GET, POST)
#     - User authentication route
#     - GET: Shows login form
#     - POST: Processes login credentials
#     - Accepts: email, password
#     - Redirects to dashboard on success
#     - Shows error message on failure
# /signup (GET, POST)
#     - New user registration route
#     - GET: Shows registration form
#     - POST: Processes new user registration
#     - Accepts: full-name, email, password
#     - Redirects to login page on success
#     - Shows error if email already exists
# /dashboard (GET)
#     - Protected user dashboard route
#     - Requires authentication
#     - Shows user's personal dashboard
#     - Redirects to login if not authenticated
#     - Displays user-specific information
# /logout (GET)
#     - User logout route
#     - Clears user session
#     - Redirects to home page
#     - Shows logout confirmation message
# /ai-test (GET, POST)
#     - AI testing interface route
#     - GET: Displays AI testing form
#     - POST: Processes uploaded document and analyzes it using AI
#     - Accepts: document file
#     - Redirects back to form on error
#     - Displays analysis result on success
# Note: All form submissions should use POST method
#       All page views should use GET method
# For CyberCoder