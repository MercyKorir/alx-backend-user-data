#!/usr/bin/env python3
"""Auth module"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hashes password"""
    salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_pwd
