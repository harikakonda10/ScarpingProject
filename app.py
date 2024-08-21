from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required

from pymongo import MongoClient
app = Flask(__name__)
# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["mydatabase"]
collection = db["mycollection"]
app.secret_key = '1c6ec12dd4a0e620de24fe963f9ea48f' # Replace with your secret key
# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
# Example user class (replace with your user model)
class User(UserMixin):
  def __init__(self, user_id):
    self.id = user_id
# Placeholder for user data (replace with your user database)
  users = {
'user1': {'password': 'password1'},
'user2': {'password': 'password2'}
  }
# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
  return User(user_id)
@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    if username in User.users and User.users[username]['password'] == password:
      user = User(username)
      login_user(user) # Log the user in
      return redirect(url_for('home')) # Redirect to home page
    return "Invalid credentials. Please try again."
  return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
# Store user data (replace with your user registration logic)
    User.users[username] = {'password': password}
    return redirect(url_for('login')) # Redirect to login page after successful registration
  return render_template('register.html')
@app.route('/', methods=["GET", "POST"])
@login_required # Requires login to access this route
def home():
  if request.method == "POST":
    job_title = request.form.get("job_title")
    location = request.form.get("location")
# Define the query based on user input
    query = {
'title': {'$regex': job_title, '$options': 'i'},
'location': {'$regex': location, '$options': 'i'}
}
# Retrieve matched documents from the collection
    matched_jobs = collection.find(query)
    return render_template('results.html', jobs=matched_jobs)
  return render_template('index.html')
if __name__ == '__main__':
  app.run(debug=True)
