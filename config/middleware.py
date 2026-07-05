import time


class RequestLoggingMiddleware:
    """
    Logs request method, path, status code,
    and response time.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        start_time = time.time()

        response = self.get_response(request)

        end_time = time.time()

        execution_time = (end_time - start_time) * 1000

        print("=" * 60)
        print(f"Method        : {request.method}")
        print(f"Endpoint      : {request.path}")
        print(f"Status Code   : {response.status_code}")
        print(f"Time Taken    : {execution_time:.2f} ms")
        print("=" * 60)

        return response