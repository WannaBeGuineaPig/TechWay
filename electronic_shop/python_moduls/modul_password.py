import hashlib

__all__ = [
    'hash_password'
]

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
