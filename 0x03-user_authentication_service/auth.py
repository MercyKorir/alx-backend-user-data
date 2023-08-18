#!/usr/bin/env python3
"""Auth module"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional


def _hash_password(password: str) -> bytes:
    """hashes password"""
    salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_pwd


def _generate_uuid() -> str:
    """generates uuid and returns it"""
    unique_id = uuid.uuid4()
    str_id = str(unique_id)
    return str_id


class Auth:
    """interacts with auth db"""

    def __init__(self) -> None:
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """creates new user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            pass
        hash_pwd = _hash_password(password)
        new_user = self._db.add_user(email, hash_pwd)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login credentials"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """creates session with session id"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        user_id = user.id
        user_uuid = _generate_uuid()
        self._db.update_user(user_id, session_id=user_uuid)
        return user_uuid

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Returns user from session_id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """destroys user session"""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            pass
        self._db.update_user(user_id, session_id=None)

    def reset_password_token(self, email: str) -> str:
        """updates the password of user"""
        try:
            user = self._db.find_user_by(email=email)
        except ValueError:
            raise ValueError("Not found")
        user_uuid = _generate_uuid()
        self._db.update_user(user.id, reset_token=user_uuid)
        return user_uuid
