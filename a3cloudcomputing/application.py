from werkzeug.security import generate_password_hash
from application import create_app, db
from application.models import User

# Create the Flask application instance
app = create_app()

def update_password_hashes():
    """
    Update password hashes for existing users if they are not in the correct format.
    
    This function iterates over all users in the database and updates their passwords
    to the correct hash format if necessary.
    """
    with app.app_context():
        users = User.query.all()
        for user in users:
            if not user.password.startswith('pbkdf2:sha256'):
                print(f"Updating password for user: {user.username}")  # Debugging
                new_hashed_password = generate_password_hash(user.password)
                user.password = new_hashed_password
                db.session.add(user)
        db.session.commit()
        print("Password hashes updated successfully")  # Debugging

@app.before_first_request
def before_first_request_func():
    """
    Run the password update logic before the first request.
    
    This function ensures that the password update is performed before the first request
    is processed by the Flask application.
    """
    update_password_hashes()

if __name__ == "__main__":
    app.run(debug=True)
