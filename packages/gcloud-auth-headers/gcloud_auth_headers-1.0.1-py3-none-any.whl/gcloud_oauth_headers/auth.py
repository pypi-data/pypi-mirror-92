import time

import google.auth.crypt
import google.auth.jwt

from gcloud_oauth_headers import SERVICE_ACCOUNT_FILE, SERVICE_ACCOUNT_EMAIL, SERVICE_NAME_AUDIENCE


def generate_jwt(sa_keyfile,
                 sa_email,
                 audience,
                 expiry_length=3600):
    now = int(time.time())

    payload = {
        'iat': now,
        "exp": now + expiry_length,
        'iss': sa_email,
        'aud': audience,
        'sub': sa_email,
        'email': sa_email
    }

    signer = google.auth.crypt.RSASigner.from_service_account_file(sa_keyfile)
    jwt = google.auth.jwt.encode(signer, payload)

    return jwt


def run(
    audience=SERVICE_NAME_AUDIENCE,
    sa_path=SERVICE_ACCOUNT_FILE,
    sa_email=SERVICE_ACCOUNT_EMAIL
):
    expiry_length = 3600
    keyfile_jwt = generate_jwt(sa_path,
                               sa_email,
                               audience,
                               expiry_length)
    return {
        'Authorization': 'Bearer {}'.format(keyfile_jwt.decode('utf-8')),
        'content-type': 'application/json'
    }
