#!/usr/bin/env python3
"""Auth module"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """hashes password"""
    salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_pwd


class Auth:
    """interacts with auth db"""

    def __init__(self) -> None:
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """creates new user"""
        try:
            ex_user = self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except ValueError:
            hash_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hash_pwd)
            return new_user
