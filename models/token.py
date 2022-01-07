import os
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from redis import Redis
from datetime import timedelta
import urllib.parse



# in production you can use Settings management
# from pydantic to get secret key from .env
class Settings(BaseModel):
    authjwt_secret_key: str = "3d781d186bbeaaec8405d529c23a18a7d9c53e3bf94b1c3ea259df93e42fbcfe"
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    access_expires: int = timedelta(minutes=15)
    refresh_expires: int = timedelta(days=30)


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()



redis_url = os.getenv('REDISTOGO_URL')
urllib.parse.uses_netloc.append('redis')
url = urllib.parse.urlparse(redis_url)
redis_conn = Redis(host=url.hostname, port=url.port, db=0, password=url.password)
# # Setup our redis connection for storing the denylist tokens
# redis_conn = Redis(host='localhost', port=6379, db=0, decode_responses=True)


# Create our function to check if a token has been revoked. In this simple
# case, we will just store the tokens jti (unique identifier) in redis.
# This function will return the revoked status of a token. If a token exists
# in redis and value is true, token has been revoked
@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    entry = redis_conn.get(jti)
    return entry and entry == 'true'
