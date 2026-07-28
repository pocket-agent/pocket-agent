import jwt

from pocket_agent.config.models import AppSettings


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


def verify_supabase_jwt(token: str, env: AppSettings) -> dict:
    secret = env.supabase_jwt_secret
    if not secret:
        raise AuthError(
            "SUPABASE_JWT_SECRET is not configured on the agent",
            status_code=503,
        )

    try:
        return jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            audience=env.supabase_jwt_audience,
        )
    except jwt.ExpiredSignatureError:
        raise AuthError("Token expired", status_code=401) from None
    except jwt.InvalidTokenError as exc:
        raise AuthError("Invalid token", status_code=401) from exc


def user_id_from_claims(claims: dict) -> str | None:
    sub = claims.get("sub")
    if sub is None:
        return None
    return str(sub)
