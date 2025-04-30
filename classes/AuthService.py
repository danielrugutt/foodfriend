from flask import request, session, jsonify, redirect, url_for, make_response
from functools import wraps
from firebase_admin import auth, credentials, initialize_app, firestore
import sys
from classes.Database import Database

class AuthService:
    database = None
    firebase_app = None
    firestore_db = None

    @classmethod
    def init(cls, app):
        """Initialize the AuthService with Firebase and the database."""
        cls.database = Database(app)
        cls.database.initialize_database()

        # Initialize Firebase Admin SDK
        cred = credentials.Certificate("firebase-auth.json")
        cls.firebase_app = initialize_app(cred)
        cls.firestore_db = firestore.client()

    @staticmethod
    def authorize():
        """Handle the /auth route for user authentication."""
        token = AuthService.get_bearer_token(request.headers.get('Authorization'))
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
                AuthService.database.check_and_create_user(uid, email)
            except Exception as e:
                print(f"Error interacting with the database: {e}", file=sys.stderr)
                return jsonify({'error': 'Internal server error'}), 500

            # Return success response
            return jsonify({'message': 'User authenticated successfully'}), 200

        except Exception as e:
            print(f"Error verifying token: {e}", file=sys.stderr)
            return jsonify({'error': 'Unauthorized'}), 401

    @staticmethod
    def get_bearer_token(auth_header):
        """Extract the Bearer token from the Authorization header."""
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        return auth_header.split(' ')[1]

    @staticmethod
    def auth_required(f):
        """Decorator to enforce authentication on routes."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def logout():
        """Handle the /logout route to log out the user."""
        session.pop('user', None)  # Remove the user from session
        response = make_response(redirect(url_for('login')))
        response.set_cookie('session', '', expires=0)  # Optionally clear the session cookie
        return response

    @staticmethod
    def delete_account():
        """Handle account deletion."""
        uid = session.get("uid")
        try:
            # Delete the user using Firebase Admin SDK
            auth.delete_user(uid)
            session.pop('user', None)  # Remove user from session
            response = make_response(redirect(url_for('login')))
            return response
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
# Exposing auth_required as a global function for use in other modules
auth_required = AuthService.auth_required