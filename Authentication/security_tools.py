import secrets
import hashlib
from User.models import User
from Authentication.models import Token
# used to encrypt the password to SHA256 when creating new user
def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


'''
checks email and password saves new token in db and returns it
'''
def login(email,  password):
    hashed_password = encrypt_string(password)
    try:
        user = User.objects.get(email=email, password_SHA256=hashed_password)

        try:
            # if already the user has a token logout from that 
            cur_token = Token.objects.get(user=user)
            cur_token.delete()
        except Token.DoesNotExist:
            pass
            
        # generate a new token and  return it
        token = secrets.token_hex()
        new_token = Token(user=user, token=token)
        new_token.save()
        return True, token 
        
    except User.DoesNotExist:
        return False, "" # return false if credential didn't match


# delete token  if exists
def logout(token):
    try:
        obj = Token.objects.get(token=token)
        obj.delete()
        return True
    except Token.DoesNotExist:
        return False



# checks if provided Authentication token is valid and returns User

def authenticate(token):
    try:
        token = Token.objects.get(token=token)
        return User.objects.get(email=token.user)
    except Token.DoesNotExist:
        return None
