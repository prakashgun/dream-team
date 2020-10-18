import os
from urllib.parse import urlparse

from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CrawlInfoSerializer


class CrawlInfoView(APIView):
    def get(self, request):
        return Response(
            {
                'message': "Input data in post"
            }
        )

    def post(self, request):
        # Validate the incoming input (provided through query parameters)
        serializer = CrawlInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the model input
        data = serializer.validated_data

        crawl_id = os.path.basename(urlparse(data['url']).path).replace('.html', '')

        return Response({
            'result': crawl_id
        })
