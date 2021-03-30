import requests

def log(get_response):
    def middleware(request):
        info_request = request

        log_info_request = (
            f"Method: {info_request.META['REQUEST_METHOD']}\n"
            f"Host: {info_request.META['HTTP_HOST']}\n"
            f"Content type:{info_request.META['CONTENT_TYPE']}\n"
            f"Content length: {info_request.META['CONTENT_LENGTH']}\n"
            f"\r\n"
            f"{info_request.body}\n"
        )

        print(log_info_request)

        response = get_response(request)

        info_response = response

        log_info_response = (
            f"Status: {info_response.status_code}\n"
            f"{info_response.content}"
        )

        print(log_info_response)

        return response
    return middleware