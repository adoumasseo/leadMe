import redis

# Configure Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
RESET_CODE_EXPIRATION = 60  # 5 minutes in seconds
