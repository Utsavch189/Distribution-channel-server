import jwt
from decouple import config

def verifyAccess(request,role):
    header=request.META.get('HTTP_AUTHORIZATION')
    try:
        jwtToken = jwt.decode((header.split(' ', 1)[1]), config('jwt_secret'), algorithms=config('jwt_algos'))
        if jwtToken['role']==role:
            return True
        else:
            return False
    except:
        pass