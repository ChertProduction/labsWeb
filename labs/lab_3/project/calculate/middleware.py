import time
import requests

def timing(get_response):
    def middleware(request):
        info_request = request
        print(info_request.META['CONTENT_TYPE'])
        response = get_response(request)
        info_response = response
        return response
    return middleware