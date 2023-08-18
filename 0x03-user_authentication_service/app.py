#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def message():
    """Return JSON payload"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """Register a user"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    try:
        user = AUTH.register_user(email, pwd)
        return jsonify({'email': email, 'message': 'user created'})
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
