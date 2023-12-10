from passlib.hash import bcrypt


def get_hashed_password(password: str) -> str:
    return bcrypt.hash(secret=password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(secret=plain_password, hash=hashed_password)
