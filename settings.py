import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import redis
sys.modules['redis'] = redis
sys.modules['redis.asyncio'] = redis
sys.modules['redis_helper'] = redis
from helpers.redis import RedisFake
Dev_FINAL = "123456789"
TOKEN = "123456789:TEST"
OWNER_ID = 5434703779
botUsername = "test_bot"
r = RedisFake(bot_id=Dev_FINAL)
class Config:
    pass
config = Config()