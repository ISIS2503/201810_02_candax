"""
    JSON Web Token auth for Tornado
"""
import jwt
import json
from six.moves.urllib.request import urlopen

AUTH0_DOMAIN = 'isis2503-sjimenez16.auth0.com'
API_AUDIENCE = 'uniandes.edu.co/candax'
ALGORITHMS = ["RS256"]
AUTHORIZATION_HEADER = 'Authorization'
AUTHORIZATION_METHOD = 'bearer'
INVALID_HEADER_MESSAGE = "invalid header authorization"
MISSING_AUTHORIZATION_KEY = "Missing authorization"
AUTHORIZATION_ERROR_CODE = 401

jwt_options = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': False,
    'verify_iat': True,
    'verify_aud': False
}


def is_valid_header(parts):
    """
        Validate the header
    """
    if parts[0].lower() != AUTHORIZATION_METHOD:
        return False
    elif len(parts) == 1:
        return False
    elif len(parts) > 2:
        return False

    return True


def return_auth_error(handler, message):
    """
        Return authorization error
    """
    handler._transforms = []
    handler.set_status(AUTHORIZATION_ERROR_CODE)
    handler.write(message)
    handler.finish()


def return_header_error(handler):
    """
        Returh authorization header error
    """
    return_auth_error(handler, INVALID_HEADER_MESSAGE)


def jwtauth(handler_class):
    """
        Tornado JWT Auth Decorator
    """
    def wrap_execute(handler_execute):
        def require_auth(handler, kwargs):

            auth = handler.request.headers.get(AUTHORIZATION_HEADER)
            print(auth)
            if auth:
                parts = auth.split()

                if not is_valid_header(parts):
                    return_header_error(handler)

                token = parts[1]
                jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
                jwks = json.loads(jsonurl.read())
                unverified_header = jwt.get_unverified_header(token)
                print('*************')
                rsa_key = {}
                print(type(jwks))
                # count = 0
                print(unverified_header)
                # for key in jwks.keys():
                #     print(count)
                #     if key["kid"] == unverified_header["kid"]:
                #         print('entrooooo')
                #         rsa_key = {
                #             "kty": key["kty"],
                #             "kid": key["kid"],
                #             "use": key["use"],
                #             "n": key["n"],
                #             "e": key["e"]
                #         }
                #
                #     count += 1

                print('---------------')
                # print(rsa_key)
                if rsa_key:
                    try:
                        payload = jwt.decode(
                            token,
                            rsa_key,
                            algorithms=ALGORITHMS,
                            audience=API_AUDIENCE,
                            issuer="https://"+AUTH0_DOMAIN+"/"
                        )
                        print(payload)
                    except Exception as err:
                        return_auth_error(handler, str(err))

            else:
                handler._transforms = []
                handler.write(MISSING_AUTHORIZATION_KEY)
                handler.finish()

            return True

        def _execute(self, transforms, *args, **kwargs):

            try:
                require_auth(self, kwargs)
            except Exception:
                return False

            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)
    return handler_class
