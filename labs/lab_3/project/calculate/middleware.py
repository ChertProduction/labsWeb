import requests

def log(get_response):
    def middleware(request):
        info_request = request

        print(info_request.META['REQUEST_METHOD'])
        print(info_request.META['HTTP_HOST'])
        print(info_request.META['CONTENT_TYPE'])
        print(info_request.META['CONTENT_LENGTH'])
        print(info_request.body)


        response = get_response(request)

        info_response = response

        print(info_response.status_code)
        print(info_response.content)


        return response
    return middleware