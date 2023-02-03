import jwt
from decouple import config
from datetime import datetime

class Verify:
    def __init__(self,request):
        self.request=request
        self.now = datetime.now()
        self.key=config('jwt_secret')
        self.algo=config('jwt_algos')

    def is_Tokenvalid(self):
        if self.request.META.get('HTTP_AUTHORIZATION'):
            header= self.request.META.get('HTTP_AUTHORIZATION')
            try:
                jwtToken = jwt.decode((header.split(' ', 1)[1]), self.key, algorithms=self.algo)
                presentTime=datetime.timestamp(self.now)
                if(jwtToken['exp']>presentTime):
                    return {
                        "info":"Ok!",
                        "status":200,
                        "token":header.split(' ', 1)[1]
                    }
                else:
                    return {
                        "info":"Token Expired",
                        "status":403
                    }
            except:
                return {
                        "info":"Token Expired",
                        "status":403
                    }
        else:
            return {
                "info":"UnAuthorized",
                "status":401
            }