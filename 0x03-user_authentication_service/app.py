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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """POST /sessions route to handle login"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(401)
    if not auth.valid_login(email, password):
        abort(401)
    session_id = auth.create_session(email)
    if not session_id:
        abort(401)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logouts user and destroy the session"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
