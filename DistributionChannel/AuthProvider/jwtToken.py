import jwt
from datetime import datetime,timedelta
from decouple import config


class JWT_Builder:
    def __init__(self,payload,enc=None):
        self.payload=payload
        self.enc=enc
        self.now = datetime.now()
        self.key=config('jwt_secret')
        self.algo=config('jwt_algos')

    def get_token(self):
        access_token_exp=datetime.timestamp(self.now+timedelta(hours=2))
        refresh_token_exp=datetime.timestamp(self.now+timedelta(hours=2.5))

        access_token=jwt.encode((self.payload|{"exp":access_token_exp,"created_at":datetime.timestamp(self.now)}),self.key,algorithm=self.algo)
        resfresh_token=jwt.encode((self.payload|{"exp":refresh_token_exp,"created_at":datetime.timestamp(self.now)}),self.key,algorithm=self.algo)
        data={
            "access_token":access_token,
            "refresh_token":resfresh_token
        }
        return (data)
    
