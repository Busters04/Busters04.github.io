from werkzeug.security import generate_password_hash, check_password_hash
from .database import usersCol

def create_user(email, password):
    """
    Creates a new user document in the users collection.
    Password is stored as a hashed string.
    """
    # Check if user already exists
    existing_user = usersCol.find_one({"email": email})
    if existing_user:
        return False  # User already exists

    hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = {
        "email": email,
        "password": hashed_pw
    }
    usersCol.insert_one(new_user)
    return True

def get_user_by_email(email):
    """
    Retrieves a user by email from the users collection.
    """
    return usersCol.find_one({"email": email})

def verify_password(hashed_password, password):
    """
    Verifies if a given password matches the hashed password.
    """
    return check_password_hash(hashed_password, password)