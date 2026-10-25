"""Tenant, audience, caller and delegated-scope validation for the MCP resource."""
import asyncio
from dataclasses import dataclass
import logging
from urllib.parse import urlsplit
from uuid import UUID

import jwt
from mcp.server.auth.provider import AccessToken

logger = logging.getLogger(__name__)
EVIDENCE_SCOPE = "Evidence.Read"


@dataclass(frozen=True)
class EntraSettings:
    tenant_id: str
    audience: str
    client_ids: frozenset[str]
    user_ids: frozenset[str]
    resource_url: str

    def __post_init__(self):
        for value in (self.tenant_id, self.audience, *self.client_ids, *self.user_ids):
            if str(UUID(value)) != value:
                raise ValueError("Entra identifiers must be canonical lowercase UUIDs")
        if not self.client_ids or not self.user_ids:
            raise ValueError("Explicit client and user allowlists are required")
        url = urlsplit(self.resource_url)
        if (url.scheme != "https" or not url.hostname or url.username or url.password
                or url.port not in (None, 443) or url.path != "/mcp"
                or url.query or url.fragment):
            raise ValueError("The public MCP resource must be an HTTPS /mcp URL")

    @property
    def issuer(self) -> str:
        return f"https://login.microsoftonline.com/{self.tenant_id}/v2.0"


class EntraTokenVerifier:
    def __init__(self, settings: EntraSettings):
        self.settings = settings
        self.keys = jwt.PyJWKClient(
            f"https://login.microsoftonline.com/{settings.tenant_id}/discovery/v2.0/keys",
            timeout=10,
        )

    def _verify(self, token: str) -> AccessToken | None:
        try:
            key = self.keys.get_signing_key_from_jwt(token)
            claims = jwt.decode(
                token, key.key, algorithms=["RS256"], audience=self.settings.audience,
                issuer=self.settings.issuer,
                options={"strict_aud": True, "require": [
                    "iss", "aud", "exp", "iat", "nbf", "tid", "oid", "azp", "scp",
                ]},
            )
            if (not all(isinstance(claims[name], str) for name in ("tid", "azp", "oid", "scp"))
                    or claims["tid"] != self.settings.tenant_id
                    or claims["azp"] not in self.settings.client_ids
                    or claims["oid"] not in self.settings.user_ids
                    or not isinstance(claims["scp"], str)
                    or EVIDENCE_SCOPE not in claims["scp"].split()):
                logger.warning("MCP bearer rejected: tenant, caller or scope mismatch")
                return None
            return AccessToken(
                token=token, client_id=claims["azp"], subject=claims["oid"],
                scopes=claims["scp"].split(), expires_at=int(claims["exp"]),
                resource=self.settings.audience,
            )
        except (jwt.InvalidTokenError, jwt.PyJWKClientError) as error:
            logger.warning("MCP bearer rejected: type=%s", type(error).__name__)
            return None

    async def verify_token(self, token: str) -> AccessToken | None:
        return await asyncio.to_thread(self._verify, token)
