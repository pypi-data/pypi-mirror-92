import jwt

def jwt_decode(*args, **kwargs):
    if args:
        xjwt, encoded_jwt = args[0].split(" ")
        return jwt.decode(encoded_jwt, args[1], algorithms=["HS256"])
    elif kwargs["token"] and kwargs["secret_key"]:
        xjwt, encoded_jwt = kwargs["token"].split(" ")
        return jwt.decode(encoded_jwt, kwargs["secret_key"], algorithms=["HS256"])
    else:
        return False