import hmac, base64, struct, hashlib, time
from django.contrib.auth.backends import ModelBackend
from django.utils.crypto import pbkdf2
from .models import User

# A custom backend to support Two-Factor authentication.
class TwoFactorAuthBackend(ModelBackend):

    def authenticate(self, session=None, user_id=None, token=None, signature=None):
        # Ensure that we have TFA parameters
        if token is None or signature is None:
            return None

        # Fetch the user
        try:
            user = User.objects.get(pk=user_id)
        except:
            return None

        # Verify the signature from the user is the one we generated
        expected_tfa_sig = base64.b16encode(pbkdf2(session.get('tfa_key', '') + user.password, session.get('tfa_salt', ''), 1000, 24))
        if expected_tfa_sig != signature:
            return None

        # Verify the token from the user
        expected_token = str(get_totp_token(user.totp_secret.upper()))
        if expected_token == token:
            return user

        return None

def get_hotp_token(secret, intervals_no):
    key = base64.b16decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(h[19]) & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

def get_totp_token(secret):
    return get_hotp_token(secret, intervals_no=int(time.time())//30)