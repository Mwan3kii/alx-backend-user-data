#!/usr/bin/env python3
"""Create basic Flask app for routes"""
from flask import Flask, jsonify, request
from flask import abort, make_response
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index():
    """Handle GET request and returns in json"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """Register a new user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """POST /sessions route to handle login"""
    # Get email and password from form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email and password are provided
    if not email or not password:
        abort(401)

    # Check valid login
    if not auth.valid_login(email, password):
        abort(401)

    # Create a new session
    session_id = auth.create_session(email)
    if not session_id:
        abort(401)

    # Create response object
    response = make_response(jsonify({"email": email, "message": "logged in"}))

    # Set session_id cookie
    response.set_cookie("session_id", session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
