from flask import Flask, flash, session, render_template, redirect, url_for, request, jsonify
from cloudinary.uploader import upload
from config import Config
from models import db, User, InsuranceDocument
import json
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
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handle user registration.
    GET: Display signup form
    POST: Process new user registration
    
    Returns:
        GET: rendered signup.html template
        POST: redirect to login page on success or back to signup on failure
    """
    if request.method == 'POST':
        # Get form data
        name = request.form.get('full-name')
        email = request.form.get('email') 
        password = request.form.get('password')
        phone = request.form.get('phone')
        occupation = request.form.get('occupation')
        dob = request.form.get('dob')
        
        # Check if user already exists with email
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('signup'))
            
        # Create new user with all fields
        new_user = User(
            name=name,
            email=email,
            password=password,  # Use password hashing later 
            phone=phone,
            occupation=occupation,
            dob=dob
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('signup.html')

# Route handler for the dashboard (protected route)
@app.route('/dashboard')
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