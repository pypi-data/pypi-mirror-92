import time

import google.auth.crypt
import google.auth.jwt

from gcloud_oauth_headers import SERVICE_ACCOUNT_EMAIL, SERVICE_ACCOUNT_FILE, SERVICE_NAME_AUDIENCE


def main():
    now = int(time.time())

    payload = {
        'iat': now,
        "exp": now + 3600,
        'iss': SERVICE_ACCOUNT_EMAIL,
        'aud': SERVICE_NAME_AUDIENCE,
        'sub': SERVICE_ACCOUNT_EMAIL,
        'email': SERVICE_ACCOUNT_EMAIL
    }

    signer = google.auth.crypt.RSASigner.from_service_account_file(SERVICE_ACCOUNT_FILE)
    jwt = google.auth.jwt.encode(signer, payload)

    print({
        'Authorization': 'Bearer {}'.format(jwt.decode('utf-8')),
        'content-type': 'application/json'
    })


if __name__ == "__main__":
    main()
