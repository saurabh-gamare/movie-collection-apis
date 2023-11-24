from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache


class RequestCount(APIView):

    def get(self, request):
        try:
            request_count = cache.get('request_count')
        except:
            return Response({'error': 'Please start your local redis server on redis://127.0.0.1:6379/1'})
        if request_count:
            return Response({'request_count': request_count})
        return Response({'request_count': 0})


class RequestCountReset(APIView):

    def post(self, request):
        try:
            cache.set('request_count', 0)
        except:
            return Response({'error': 'Please start your local redis server on redis://127.0.0.1:6379/1'})
        return Response({'message': 'request count reset successfully'
})
