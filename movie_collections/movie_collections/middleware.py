from django.core.cache import cache


class RequestCountMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            request_count = cache.get('request_count') or 0
            request_count += 1
            cache.set('request_count', request_count)
        except:
            pass
        response = self.get_response(request)
        return response