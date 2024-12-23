import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"

def create_token(data, expires_in=600):
    payload = {
        "data": data,
        "exp": datetime.utcnow() + timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
