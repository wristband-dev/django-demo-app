# ====================================================================
# ⚠️  DANGER ZONE - WRISTBAND INTERNAL DEVELOPMENT ONLY ⚠️
# ====================================================================
# This module globally disables SSL verification for ALL HTTP requests
# in this Python process. This is EXTREMELY DANGEROUS and should only
# be used by Wristband internal developers for local testing.
#
# NEVER ENABLE THIS IN:
# - Production environments
# - Customer deployments
# - Public hosted demos
# - Any environment with real user data
#
# This exists solely because local Wristband development environments
# don't have valid SSL certificates, similar to how Node.js developers
# use NODE_TLS_REJECT_UNAUTHORIZED=0 for local development.
# ====================================================================
import logging
from typing import Any, Callable

import httpx

logger = logging.getLogger(__name__)

# 🚨 TOGGLE THIS FLAG FOR LOCAL DEVELOPMENT ONLY 🚨
# Set to False before any production deployment or public demo
_DISABLE_SSL_FOR_WRISTBAND_DEV = False  # ⚠️ CHANGE TO False FOR PRODUCTION ⚠️

if _DISABLE_SSL_FOR_WRISTBAND_DEV:
    logger.warning("🚨 WARNING: SSL verification is DISABLED for ALL httpx requests!")
    logger.warning("🚨 This is for Wristband internal development only!")
    logger.warning("🚨 DO NOT USE IN PRODUCTION!")

    # Patch httpx.Client.__init__ to use unverified SSL by default
    original_httpx_client_init = httpx.Client.__init__

    def patched_httpx_client_init(self: httpx.Client, *args: Any, **kwargs: Any) -> None:
        # If verify is not explicitly set, disable it
        if "verify" not in kwargs:
            kwargs["verify"] = False
        return original_httpx_client_init(self, *args, **kwargs)

    httpx.Client.__init__ = patched_httpx_client_init  # type: ignore[method-assign]

    # Patch httpx module-level functions
    original_httpx_post: Callable[..., httpx.Response] = httpx.post
    original_httpx_get: Callable[..., httpx.Response] = httpx.get

    def patched_httpx_post(*args: Any, **kwargs: Any) -> httpx.Response:
        kwargs.setdefault("verify", False)
        return original_httpx_post(*args, **kwargs)

    def patched_httpx_get(*args: Any, **kwargs: Any) -> httpx.Response:
        kwargs.setdefault("verify", False)
        return original_httpx_get(*args, **kwargs)

    httpx.post = patched_httpx_post
    httpx.get = patched_httpx_get

    logger.warning("🚨 SSL verification disabled for all httpx requests!")

# ====================================================================
# END WRISTBAND INTERNAL DEV CONFIGURATION
# ====================================================================
