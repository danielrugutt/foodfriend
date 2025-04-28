from flask import request, session, jsonify, redirect, url_for, make_response
from functools import wraps
from firebase_admin import auth
import sys
from classes.Database import Database

database = None  # Initialize this in app.py

def init_auth_service(db_instance):
    """Initialize the database instance for auth_service."""
    global database
    database = db_instance

def get_bearer_token(auth_header):
    """Extract the Bearer token from the Authorization header."""
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    return auth_header.split(' ')[1]

def authorize():
    """Handle the /auth route for user authentication."""
    token = get_bearer_token(request.headers.get('Authorization'))
    if not token:
        return jsonify({'error': 'Authorization header missing or invalid'}), 401

    try:
        # Validate the token
        decoded_token = auth.verify_id_token(token, check_revoked=True, clock_skew_seconds=60)
        uid = decoded_token['uid']
        email = decoded_token.get('email')

        # Add user to session
        session['user'] = {'uid': uid, 'email': email}
        session['uid'] = uid

        # Ensure user exists in the local database
        try:
            print(f"Creating/checking user with UID: {uid}, email: {email}")
            database.check_and_create_user(uid, email)
        except Exception as e:
            print(f"Error interacting with the database: {e}", file=sys.stderr)
            return jsonify({'error': 'Internal server error'}), 500

        # Return success response
        return jsonify({'message': 'User authenticated successfully'}), 200

    except Exception as e:
        print(f"Error verifying token: {e}", file=sys.stderr)
        return jsonify({'error': 'Unauthorized'}), 401

def auth_required(f):
    """Decorator to enforce authentication on routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def logout():
    """Handle the /logout route to log out the user."""
    session.pop('user', None)  # Remove the user from session
    response = make_response(redirect(url_for('login')))
    response.set_cookie('session', '', expires=0)  # Optionally clear the session cookie
    return response