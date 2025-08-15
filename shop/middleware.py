import logging
import time
from typing import Callable
from django.http import HttpRequest, HttpResponse

logger = logging.getLogger("requests")

class RequestLogMiddleware:
    """Логируем метод, путь, статус и время обработки."""
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start = time.perf_counter()
        response = self.get_response(request)
        duration_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "%s %s -> %s (%.1f ms)",
            request.method,
            request.get_full_path(),
            getattr(response, "status_code", "-"),
            duration_ms,
        )
        return response
