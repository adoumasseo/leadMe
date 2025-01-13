"""" A module for generate a code, store it in redis and send a mail"""

import random
from redis_config import redis_client, RESET_CODE_EXPIRATION

def generate_reset_code():
    """Generate a 6-digit verification code."""
    return f"{random.randint(100000, 999999)}"

def store_reset_code(email):
    """Store the reset code in Redis with an expiration time."""
    reset_code = generate_reset_code()
    old_code = redis_client.get(f"reset_code:{email}")
    if old_code:
        redis_client.delete(f"reset_code:{email}")
    redis_client.setex(f"reset_code:{email}", RESET_CODE_EXPIRATION, reset_code.encode('utf-8'))
    return reset_code
