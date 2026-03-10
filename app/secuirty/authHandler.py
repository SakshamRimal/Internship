import os
import datetime

import jwt
from dotenv import load_dotenv

# load .env from the app directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

JWT_SECRET_KEY = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

#static class call the method without instantiating it
class AuthHandler(object):

    @staticmethod
    # jwt have payload , userid , header
    # this will create a token jwt token with using the algorithm
    def sign_jwt(user_id : int):
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, JWT_SECRET_KEY , algorithm=JWT_ALGORITHM)
        return token

    @staticmethod
    def decode_jwt(token: str) -> dict:
        try:
            decode_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return decode_token
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except Exception as e:
            print("Unable to decode token" , e)
            return None