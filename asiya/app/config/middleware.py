import json
import logging

from django.http import RawPostDataException
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("api.errors")

_SENSITIVE_KEYS = {"password", "token", "access", "refresh", "authorization"}
_MAX_BODY_LENGTH = 3000


def _mask_sensitive_data(value):
    if isinstance(value, dict):
        return {
            key: ("***" if str(key).lower() in _SENSITIVE_KEYS else _mask_sensitive_data(item))
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_mask_sensitive_data(item) for item in value]
    return value


def _safe_request_body(request):
    if request.method in ("GET", "HEAD", "OPTIONS"):
        return None

    try:
        body_bytes = request.body
    except RawPostDataException:
        return "[unavailable: request body stream already consumed]"

    if not body_bytes:
        return None

    raw_body = body_bytes.decode("utf-8", errors="replace")
    if len(raw_body) > _MAX_BODY_LENGTH:
        raw_body = f"{raw_body[:_MAX_BODY_LENGTH]}...[truncated]"

    content_type = request.META.get("CONTENT_TYPE", "")
    if "application/json" not in content_type:
        return raw_body

    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError:
        return raw_body
    return _mask_sensitive_data(parsed)


def _request_context(request):
    return {
        "method": request.method,
        "path": request.get_full_path(),
        "user_id": getattr(request.user, "id", None) if getattr(request, "user", None) and request.user.is_authenticated else None,
        "remote_addr": request.META.get("REMOTE_ADDR"),
        "body": _safe_request_body(request),
    }


class ApiExceptionLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logger.exception(
            "Unhandled API exception | context=%s",
            json.dumps(_request_context(request), ensure_ascii=False, default=str),
        )
        return None

    def process_response(self, request, response):
        if response.status_code >= 500:
            logger.error(
                "API returned 5xx response | context=%s",
                json.dumps(
                    {
                        **_request_context(request),
                        "status_code": response.status_code,
                    },
                    ensure_ascii=False,
                    default=str,
                ),
            )
        return response
