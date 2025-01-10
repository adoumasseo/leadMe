"""" A module for generate a code, store it in redis and send a mail"""

import random, os
from redis_config import redis_client

def generate_reset_code():
    """Generate a 6-digit verification code."""
    return f"{random.randint(100000, 999999)}"

def store_reset_code(email):
    """Store the reset code in Redis with an expiration time."""
    reset_code = generate_reset_code()
    redis_client.setex(f"reset_code:{email}", int(os.getenv('RESET_CODE_EXPIRATION', 300)), reset_code)
    return reset_code
