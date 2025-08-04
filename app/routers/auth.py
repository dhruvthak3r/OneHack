
import jwt
from jwt import PyJWKClient

from dotenv import load_dotenv

import os


load_dotenv()


AUTH0_CLIENT_ID = os.getenv("auth0_client_id")
AUTH0_CLIENT_SECRET = os.getenv("auth0_client_secret")
AUTH0_DOMAIN = os.getenv("auth0_domain")
API_AUDIENCE = os.getenv("auth0_api_audience")
ALGORITHMS = ["RS256"]

if not all([AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_DOMAIN]):
    raise RuntimeError("Missing one or more Auth0 environment variables.")


def verify_jwt_token(token: str):
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    jwks_client = PyJWKClient(jwks_url)
    signing_key = jwks_client.get_signing_key_from_jwt(token)

    decoded_token = jwt.decode(
        token,
        signing_key.key,
        algorithms=ALGORITHMS,
        audience=API_AUDIENCE,
        issuer=f"https://{AUTH0_DOMAIN}/",
    )
    return decoded_token