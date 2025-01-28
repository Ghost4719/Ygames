from django.conf import settings

class AssetPathMiddleware:
    def __init__(self, get_response):
        # Initialize the middleware with the `get_response` callable
        self.get_response = get_response

    def __call__(self, request):
        # This is where the request is processed, and you can modify the response
        response = self.get_response(request)  # Call the next middleware or view
        return self.process_response(request, response)

    def process_response(self, request, response):
        # Modify the response here
        if 'Content-Type' in response and response['Content-Type'].startswith('text/html'):
            # Your asset path processing logic here
            pass
        return response
