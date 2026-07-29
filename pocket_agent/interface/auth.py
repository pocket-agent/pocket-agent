import jwt
from jwt import PyJWKClient

from pocket_agent.config.models import AppSettings

try:
    from pocket_agent_sdk.auth import local_dev_claims
except ImportError:
    local_dev_claims = None  # type: ignore[assignment,misc]

_GOOGLE_JWKS = PyJWKClient("https://www.googleapis.com/oauth2/v3/certs")
_GOOGLE_ISSUERS = ["https://accounts.google.com", "accounts.google.com"]


class AuthError(Exception):
    def __init__(self, message: str, status_code: int = 401) -> None:
        super().__init__(message)
        self.status_code = status_code


def extract_bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    token = parts[1].strip()
    return token or None


def is_local_auth(env: AppSettings) -> bool:
    return env.auth_mode.strip().lower() == "none"


def local_user_claims() -> dict:
    if local_dev_claims is not None:
        return local_dev_claims()
    return {
        "sub": "local-dev",
        "email": "local@pocket-agent.dev",
        "name": "Local User",
    }


def verify_google_id_token(token: str, env: AppSettings) -> dict:
    client_id = env.google_client_id.strip()
    if not client_id:
        raise AuthError(
            "GOOGLE_CLIENT_ID is not configured on the agent",
            status_code=503,
        )

    try:
        signing_key = _GOOGLE_JWKS.get_signing_key_from_jwt(token)
        return jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=client_id,
            issuer=_GOOGLE_ISSUERS,
        )
    except jwt.ExpiredSignatureError:
        raise AuthError("Token expired", status_code=401) from None
    except jwt.InvalidTokenError as exc:
        raise AuthError("Invalid token", status_code=401) from exc


def resolve_user_claims(request_authorization: str | None, env: AppSettings) -> dict:
    if is_local_auth(env):
        return local_user_claims()

    token = extract_bearer_token(request_authorization)
    if not token:
        raise AuthError("Missing bearer token")
    return verify_google_id_token(token, env)


def user_id_from_claims(claims: dict) -> str | None:
    sub = claims.get("sub")
    if sub is None:
        return None
    return str(sub)
