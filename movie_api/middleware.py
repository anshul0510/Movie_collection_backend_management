from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

class RequestCounterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not cache.get('request_count'):
            cache.set('request_count', 0)

        cache.incr('request_count')

class RequestCountResetMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'POST' and request.path == '/request-count/reset/':
            cache.set('request_count', 0)
