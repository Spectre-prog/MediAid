from flask import Flask, flash, session, render_template, redirect, url_for, request, jsonify
from cloudinary.uploader import upload
from config import *
from models import *
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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

    # Check if user already exists with email
    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "User already exists"})
        
    # Create new user with all fields
    new_user = User(
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
        flash('Please login first', 'error')
        return redirect(url_for('login'))
        
    user = User.query.get(session['user_id'])
    return render_template('user_dashboard.html', user=user)

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